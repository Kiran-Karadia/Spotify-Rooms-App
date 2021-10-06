import React, { Component } from "react";
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";

export default class JoinRoomPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      room_code: "",
      error: "",
    };
  }

  render() {
    return (
      <Grid container spacing={1} align="center">
        <Grid item xs={12}>
          <Typography variant="h4" component="h4">
            Join a Room
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <TextField
            errormessage={this.state.error}
            label="Room Code"
            placeholder="Enter a room code"
            value={this.state.room_code}
            helperText={this.state.error}
            variant="outlined"
            onChange={this.handleTextFieldChange}
          />
        </Grid>
        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            onClick={this.enterRoomBtnClicked}
          >
            Enter Room
          </Button>
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }

  handleTextFieldChange = (e) => {
    // Underscore denotes this is a private function
    this.setState({
      room_code: e.target.value,
    });
  };

  enterRoomBtnClicked = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        room_code: this.state.room_code,
      }),
    };
    fetch("/api/join-room", requestOptions)
      .then((response) => {
        if (response.ok) {
          this.props.history.push(`/room/${this.state.room_code}`);
        } else {
          this.setState({ error: "Room not found!" });
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };
}
