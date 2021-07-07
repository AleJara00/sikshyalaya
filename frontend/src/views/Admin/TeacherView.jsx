import React, { useState, useEffect } from "react";
import * as yup from "yup";
import Grid from "@material-ui/core/Grid";
import colorscheme from "../../utils/colors";
import DashboardLayout from "../../components/DashboardLayout/DashboardLayout";
import Students from "./components/Student";
import { GoPlus } from "react-icons/go";
import "./statics/css/commonView.css";
import useAPI from "../../utils/useAPI";
import CustomButton from "../../components/CustomButton";
import { ImCross } from "react-icons/im";
import { Formik, Form } from "formik";
import callAPI from "../../utils/API";
import CustomTextField from "../../components/CustomTextField";
import { useHistory } from "react-router-dom";
import { DatePicker } from "../../components/CustomDateTime";

const validationSchema = yup.object({
  full_name: yup.string("Enter your name").required("Name is required"),
  address: yup.string("Enter your address").required("Address is required"),
  join_year: yup.number("Enter Joined Year").required("Join year is required"),
  dob: yup.string("Enter Date of Birth").required("Date of Birth is required"),
  phone_number: yup.number().typeError("Not a valid phone number"),
  email: yup
    .string("Enter your email")
    .email("Enter a valid email!")
    .required("Email is required"),
  semester: yup.number().required("Semester is required"),
  program: yup.number().required("Program is required"),
});

const semester = [
  { name: "I", value: 1 },
  { name: "II", value: 2 },
  { name: "III", value: 3 },
  { name: "IV", value: 4 },
  { name: "V", value: 5 },
  { name: "VI", value: 6 },
  { name: "VII", value: 7 },
  { name: "VIII", value: 8 },
];

const TeacherView = ({ location, ...rest }) => {
  const history = useHistory();
  const [isPopUp, setPopUp] = useState(false);
  const [editState, setEditState] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  const teacherFormatter = (values) => {
    return values.data.map((item) => {
      return {
        id: item.id,
        name: item.full_name,
      };
    });
  };
  const teacherEditFormatter = (values) => {
    return {
      id: values.data.id,
      full_name: values.data.full_name,
      email: values.data.email,
      dob: values.data.dob,
      address: values.data.address,
      contact_number: values.data.contact_number,
      join_year: values.data.join_year,
    };
  };
  const teacherDefault = [];
  const [students] = useAPI(
    { endpoint: `/api/v1/users/teacher/` },
    teacherFormatter,
    teacherDefault
  );

  const programFormatter = (value) =>
    value.data.map((item) => ({
      name: item.name,
      value: item.id,
    }));

  const groupFormatter = (value) => {
    return value.data;
  };

  const [group] = useAPI({ endpoint: "/api/v1/group/all/" }, groupFormatter);

  const [program] = useAPI({ endpoint: "/api/v1/program/" }, programFormatter);

  const onSubmit = async (data) => {
    let group_id_list = group.filter((item) => {
      if (item.sem === data.semester && item.program.id === data.program) {
        return item;
      }
    });

    if (!group_id_list.length) {
      throw "No matching group found!";
    }
    let group_id = group_id_list[0].id;

    let req_data = {
      email: data.email,
      full_name: data.full_name,
      address: data.address,
      group_id: group_id,
      contact_number: data.phone_number,
      dob: data.dob,
      join_year: parseInt(data.join_year),
    };

    let response;
    if (!editState) {
      response = await callAPI({
        endpoint: "/api/v1/auth/signup",
        method: "POST",
        data: req_data,
      });
      students.push({
        name: req_data.full_name,
        id: response.data.id,
      });
    } else {
      response = await callAPI({
        endpoint: `/api/v1/users/${selectedUser.id}`,
        method: "PUT",
        data: req_data,
      });
      const position = students.findIndex(
        (currentValue) => currentValue.id == selectedUser.id
      );
      students[position] = {
        name: req_data.full_name,
        id: selectedUser.id,
      };
    }

    if (response.status && response.status == 200) {
      setPopUp(false);
      setEditState(false);
      setSelectedUser(null);
    }
  };

  const loadUser = async (id) => {
    const postResponse = teacherEditFormatter(
      await callAPI({
        endpoint: `/api/v1/users/${id}`,
        method: "GET",
      })
    );
    setSelectedUser(postResponse);
  };

  return (
    <DashboardLayout>
      <Grid
        container
        direction="column"
        justify="flex-start"
        alignItems="center"
        className="adminCommon_root"
        wrap="nowrap"
      >
        <Grid item className="adminCommon_topBarContainer">
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="center"
            className="adminCommon_topBar"
          >
            <Grid xs item className="adminCommon_textContainer">
              <p className="adminCommon_text">Teachers</p>
            </Grid>
            <Grid xs={1} item className="adminCommon_plusIcon">
              <div className="adminCommon_plusIconContainer">
                <GoPlus
                  size={25}
                  color={colorscheme.green2}
                  onClick={() => {
                    setPopUp(true);
                  }}
                />
              </div>
            </Grid>
          </Grid>
        </Grid>

        <Grid item className="adminCommon_botBar">
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
            className="adminCommon_innerContainer"
            wrap="wrap"
          >
            {students.map((item) => (
              <Grid xs={6} item key={item.id}>
                <Students
                  key={item.id}
                  name={item.name}
                  onEdit={() => {
                    setEditState(true);
                    setPopUp(true);
                    loadUser(item.id);
                  }}
                />
              </Grid>
            ))}
          </Grid>
        </Grid>
        <br />
        <br />
      </Grid>
      {isPopUp ? (
        <Grid
          container
          justify="center"
          className="adminTeacher_popUpContainer"
        >
          <Grid item className="adminTeacher_popUpBox">
            <Grid container direction="column" className="adminTeacher_formBox">
              <Formik
                enableReinitialize={true}
                initialValues={
                  selectedUser
                    ? {
                        full_name: selectedUser.full_name,
                        address: selectedUser.address,
                        program: selectedUser.program,
                        semester: selectedUser.semester,
                        join_year: selectedUser.join_year,
                        dob: selectedUser.dob,
                        email: selectedUser.email,
                        phone_number: selectedUser.contact_number,
                      }
                    : {
                        full_name: "",
                        address: "",
                        program: "",
                        semester: "",
                        join_year: "",
                        dob: null,
                        phone_number: "",
                        email: "",
                        password: "",
                        confirm_password: "",
                      }
                }
                validationSchema={validationSchema}
                onSubmit={onSubmit}
              >
                <Form>
                  <Grid
                    container
                    direction="row"
                    justify="flex-start"
                    alignItems="flex-start"
                  >
                    <Grid item xs={6} style={{ padding: "0px 20px 0px 0px" }}>
                      <CustomTextField
                        name="full_name"
                        type="text"
                        placeHolder="Full Name"
                        id="full_name"
                        addStyles="adminTeacher_inputButton"
                      />
                    </Grid>
                    <Grid item xs={6}>
                      <CustomTextField
                        name="address"
                        type="text"
                        placeHolder="Address"
                        id="address"
                        addStyles="adminTeacher_inputButton"
                      />
                    </Grid>
                    <Grid item xs={6} style={{ padding: "0px 20px 0px 0px" }}>
                      <CustomTextField
                        id="join_year"
                        name="join_year"
                        placeHolder="Join"
                        label="Join year"
                        type="text"
                        className="adminTeacher_inputButton"
                      />
                    </Grid>
                    <Grid item xs={6}>
                      <DatePicker
                        id="dob"
                        label="Birth Date"
                        className="adminTeacher_inputButton"
                      />
                    </Grid>
                    <Grid item xs={12}>
                      <CustomTextField
                        name="phone_number"
                        type="text"
                        placeHolder="Phone Number"
                        id="phone_number"
                        addStyles="adminTeacher_inputButton"
                        autoComplete="on"
                      />
                    </Grid>
                    <Grid item xs={12}>
                      <CustomTextField
                        name="email"
                        type="text"
                        placeHolder="Email"
                        id="email"
                        addStyles="adminTeacher_inputButton"
                        autoComplete="on"
                      />
                    </Grid>
                    <Grid item className="adminTeacher_submitButtonContainer">
                      <CustomButton
                        name="Save"
                        type="submit"
                        addStyles="adminTeacher_submitButton"
                      />
                    </Grid>
                  </Grid>
                </Form>
              </Formik>
            </Grid>
            <Grid item className="adminSchool_closeButtonContainer">
              <ImCross
                color={colorscheme.red3}
                className="adminSchool_closeButton"
                onClick={() => {
                  setPopUp(false);
                  setEditState(false);
                  setSelectedUser(null);
                }}
              />
            </Grid>
          </Grid>
        </Grid>
      ) : (
        <></>
      )}
    </DashboardLayout>
  );
};

export default TeacherView;
