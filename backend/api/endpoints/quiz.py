from typing import Any, List, Dict

from random import randint

import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.config import settings

from models import User
from utils import deps
from cruds import crud_quiz, crud_question
from schemas import (
    Quiz,
    QuizCreate,
    QuizUpdate,
    QuizAnswer,
    QuizAnswerCreate,
    QuizAnswerUpdate,
    QuizQuestion,
    QuizQuestionCreate,
    QuizQuestionUpdate,
)

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import aiofiles

router = APIRouter()

QUIZ_QUESTION_UPLOAD_DIR: str = "question_image"
QUIZ_OPTION_UPLOAD_DIR: str = "option_image"


@router.get("/", response_model=List[Quiz])
async def get_quiz(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    quiz = crud_quiz.get_multi(db, skip=skip, limit=limit)

    if current_user.user_type == settings.UserType.STUDENT.value:
        quiz_list = []
        for quizItem in quiz:
            if quizItem.group_id == current_user.group_id:
                quiz_list.append(quizItem)

        return quiz_list

    if current_user.user_type == settings.UserType.TEACHER.value:

        quiz_list = []
        for quizItem in quiz:
            for instructor in quizItem.instructor:
                if current_user.id == instructor.id:
                    quiz_list.append(quizItem)
        return quiz_list

    if current_user.user_type <= settings.UserType.ADMIN.value:
        return quiz


@router.post("/")
async def create_quiz(
    db: Session = Depends(deps.get_db),
    *,
    obj_in: QuizCreate,
    current_user: User = Depends(deps.get_current_active_teacher_or_above),
) -> Any:
    quiz = crud_quiz.create(db, obj_in=obj_in)
    return {"msg": "success"}


@router.get("/{id}", response_model=Quiz)
async def get_specific_quiz(
    db: Session = Depends(deps.get_db),
    *,
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    if current_user.user_type == settings.UserType.STUDENT.value:
        quiz_list = await get_quiz(db=db, current_user=current_user)
        for quiz in quiz_list:
            if quiz.id == id:
                return quiz
        raise HTTPException(
            status_code=401, detail="Error ID: 133"
        )  # not accessible by the Student user

    if current_user.user_type == settings.UserType.TEACHER.value:
        quiz_list = await get_quiz(db=db, current_user=current_user)
        for quiz in quiz_list:
            if quiz.id == id:
                return quiz
        raise HTTPException(
            status_code=401, detail="Error ID: 134"
        )  # not accessible by the Teacher user

    if current_user.user_type <= settings.UserType.ADMIN.value:
        quiz = crud_quiz.get(db, id)
        return quiz


@router.put("/{id}", response_model=QuizUpdate)
async def update_quiz(
    db: Session = Depends(deps.get_db),
    *,
    id: int,
    obj_in: QuizUpdate,
    current_user: User = Depends(deps.get_current_active_teacher_or_above),
) -> Any:
    quiz = crud_quiz.get(db, id)
    quiz = crud_quiz.update(db, db_obj=quiz, obj_in=obj_in)
    return quiz


@router.get("/{quizid}/question", response_model=List[QuizQuestion])
async def get_question(
    db: Session = Depends(deps.get_db),
    *,
    quizid: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    quiz = await get_specific_quiz(db, id=quizid, current_user=current_user)
    if not quiz:
        raise HTTPException(
            status_code=404, detail="Error ID = 135"
        )  # quiz not found in database

    questions = crud_question.get_all_by_quiz_id(db, quiz_id=quiz.id)
    return questions


@router.get("/{quizid}/question/{id}", response_model=QuizQuestion)
async def get_specific_question(
    db: Session = Depends(deps.get_db),
    *,
    quizid: int,
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    questions = await get_question(db, quizid=quizid, current_user=current_user)
    for question in questions:
        if question.id == id:
            return question

    raise HTTPException(
        status_code=404, detail="Error ID: 136"
    )  # question specific to that id not found


@router.post("/{quizid}/question")
async def create_question(
    db: Session = Depends(deps.get_db),
    *,
    quizid: int,
    obj_in: QuizQuestionCreate,
    current_user: User = Depends(deps.get_current_active_teacher_or_above),
) -> Any:
    # FIXME: is this needed?
    obj_in.quiz_id = quizid
    question = crud_question.create(db, obj_in=obj_in)

    current_directory = os.getcwd()

    FILE_PATH_QUESTION = os.path.join(
        "static", QUIZ_QUESTION_UPLOAD_DIR, f"{quizid}/{question.id}"
    )

    FILE_PATH_QUESTION = os.path.join(current_directory, FILE_PATH_QUESTION)

    FILE_PATH_OPTION = os.path.join(
        "static", QUIZ_OPTION_UPLOAD_DIR, f"{quizid}/{question.id}"
    )
    FILE_PATH_OPTION = os.path.join(current_directory, FILE_PATH_OPTION)

    if not os.path.exists(FILE_PATH_QUESTION):
        os.makedirs(FILE_PATH_QUESTION)

    if not os.path.exists(FILE_PATH_OPTION):
        os.makedirs(FILE_PATH_OPTION)

    return {"msg": "success"}


@router.put("/{quizid}/question/{id}")
async def update_question(
    db: Session = Depends(deps.get_db),
    *,
    quizid: int,
    obj_in: QuizQuestionUpdate,
    current_user: User = Depends(deps.get_current_active_teacher_or_above),
) -> Any:
    question = crud_question.get(db, id)
    if question.quiz_id == quizid:
        question = crud_question.update(db, db_obj=question, obj_in=obj_in)
        return question
    else:
        raise HTTPException(
            status_code=401, detail="Error ID = 137"
        )  # noqa Access Denied!


# XXX: ENDPOINTS for questions to write and read files and answers to those files


# FIXME: Uploaded files directory fix it
@router.post("{quizid}/question/{id}/question_image/")
async def create_question_files(
    db: Session = Depends(deps.get_db),
    files: List[UploadFile] = File(...),
    current_user=Depends(deps.get_current_active_teacher_or_above),
    *,
    quizid: int,
    id: int,
):
    # TODO: check if the file is an image?
    question = await get_specific_question(
        db, quizid=quizid, id=id, current_user=current_user
    )
    current_directory = os.getcwd()
    FILE_PATH = os.path.join("static", QUIZ_QUESTION_UPLOAD_DIR, f"{quizid}/{id}")
    FILE_PATH = os.path.join(current_directory, FILE_PATH)

    for file in files:
        filename = f"{FILE_PATH}/{file.filename}"
        async with aiofiles.open(filename, mode="wb") as f:
            content = await file.read()
            await f.write(content)

    obj_in = QuizQuestionUpdate(question_image=[file.filename for file in files])
    print(obj_in)
    updated = crud_question.update(db=db, db_obj=question, obj_in=obj_in)

    return updated


@router.post("{quizid}/question/{id}/option_image/")
async def create_option_files(
    db: Session = Depends(deps.get_db),
    files: List[UploadFile] = File(...),
    current_user=Depends(deps.get_current_active_teacher_or_above),
    *,
    quizid: int,
    id: int,
):

    # TODO: check if the file is an image?
    question = await get_specific_question(
        db, quizid=quizid, id=id, current_user=current_user
    )

    FILE_PATH = os.path.join("static", QUIZ_OPTION_UPLOAD_DIR, f"{quizid}/{id}")
    current_directory = os.getcwd()
    FILE_PATH = os.path.join(current_directory, FILE_PATH)

    for file in files:
        filename = f"{FILE_PATH}/{file.filename}"
        async with aiofiles.open(filename, mode="wb") as f:
            content = await file.read()
            await f.write(content)

    obj_in = QuizQuestionUpdate(option_image=[file.filename for file in files])
    print(obj_in)
    updated = crud_question.update(db=db, db_obj=question, obj_in=obj_in)

    return updated


@router.get("/{quizid}/question/{id}/{type}/{filename}")
async def get_image(
    db: Session = Depends(deps.get_db),
    *,
    quizid: int,
    id: int,
    filename: str,
    type: int,
    current_user: User = Depends(deps.get_current_active_user),
):
    question = await get_specific_question(
        db, quizid=quizid, id=id, current_user=current_user
    )

    if not question:
        raise HTTPException(status_code=404, detail="Error ID: 138")
        # question not found error

    if type == 1:
        if filename in question.question_image:
            FILE_PATH = os.path.join(
                "static", QUIZ_QUESTION_UPLOAD_DIR, f"{quizid}/{id}"
            )
        else:
            raise HTTPException(
                status_code=401, detail="Error ID: 139"
            )  # file not of that question

    if type == 2:
        if filename in question.option_image:
            FILE_PATH = os.path.join("static", QUIZ_OPTION_UPLOAD_DIR, f"{quizid}/{id}")
        else:
            raise HTTPException(
                status_code=401, detail="Error ID: 140"
            )  # file not of that question

    BACKEND_ROOT = os.getcwd()
    FILE_PATH = os.path.join(BACKEND_ROOT, FILE_PATH, filename)

    if os.path.isfile(FILE_PATH):
        file = FileResponse(f"{FILE_PATH}")
        return file
    else:
        raise HTTPException(
            status_code=404, detail="Error ID: 141"
        )  # no file exist in the path
