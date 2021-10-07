import React, { Component } from "react";
import JoinRoomPage from "./JoinRoomPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      room_code: null,
    };
  }

  // Called at start of component rendering
  // Asynchronous: page will render first and then update once this function is done
  async componentDidMount() {
    fetch("/api/user-in-room")
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          room_code: data.room_code,
        });
      });
  }
  // Seperate function just to make code more readable
  renderHomePage() {
    return (
      <Grid container spacing={3} align="center">
        <Grid item xs={12}>
          <Typography variant="h3" compact="h3">
            House Party
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <ButtonGroup disableElevation variant="contained" color="primary">
            <Button color="primary" to="/join" component={Link}>
              Join a Room
            </Button>
            <Button color="secondary" to="/create" component={Link}>
              Create a Room
            </Button>
          </ButtonGroup>
        </Grid>
      </Grid>
    );
  }

  clearRoomCode = () => {
    this.setState({
      room_code: null,
    });
  };
  render() {
    // Create a switch statement that routes to the correct page depending on the current url
    // Need the 'exact' word since it is being checked first and it will consider '/xxx' to match with '/'
    return (
      <Router>
        <Switch>
          <Route
            exact
            path="/"
            render={() => {
              return this.state.room_code ? (
                <Redirect to={`/room/${this.state.room_code}`} />
              ) : (
                this.renderHomePage()
              );
            }}
          ></Route>
          <Route path="/join" component={JoinRoomPage} />
          <Route path="/create" component={CreateRoomPage} />
          <Route
            path="/room/:room_code"
            render={(props) => {
              return <Room {...props} leaveRoomCallback={this.clearRoomCode} />;
            }}
          />
        </Switch>
      </Router>
    );
  }
}
