import axios from "axios";

const updateHeaders = () => {
  axios.defaults.headers.post["Content-Type"] = "multipart/form-data";
};

updateHeaders();


export default axios;
