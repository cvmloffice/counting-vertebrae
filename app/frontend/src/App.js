import React, { useEffect } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import ImageDisplay from "./screens/imageDisplay";

const App = () => {
  useEffect(() => {}, []);

  return (
    <Router>
      <Switch>
        <Route exact path="/" component={ImageDisplay} />
      </Switch>
    </Router>
  );
};

export default App;
