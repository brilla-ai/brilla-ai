import React from "react";
import "./App.scss";

export default class App extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {}

  render() {
    return (
      <div className="App container">
        <div className="container-fluid">
          <div className="row">
            <div className="col-xs-12 col-sm-8 col-md-8 offset-md-2">
              <h1>NSMQ AI</h1>
              <div className="nsmq-app">
                <h2>Work In Progress...</h2>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
