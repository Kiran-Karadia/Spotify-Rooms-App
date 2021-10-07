import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { Collapse } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";

export default class CreateRoomPage extends Component {
  static defaultProps = {
    can_pause: false,
    votes_to_skip: 2,
    update: false,
    room_code: null,
    updateCallback: () => {},
  };

  constructor(props) {
    super(props);
    this.state = {
      can_pause: this.props.can_pause,
      votes_to_skip: this.props.votes_to_skip,
      error_msg: "",
      success_msg: "",
    };
  }

  handleVotesChange = (e) => {
    this.setState({
      votes_to_skip: e.target.value,
    });
  };

  handleCanPauseChange = (e) => {
    this.setState({
      can_pause: e.target.value === "true" ? true : false,
    });
  };

  handleCreateRoomBtnClicked = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: this.state.votes_to_skip,
        can_pause: this.state.can_pause,
      }),
    };
    fetch("/api/create-room", requestOptions)
      .then((response) => response.json())
      .then((data) => this.props.history.push("/room/" + data.room_code));
  };

  handleUpdateBtnClicked = () => {
    const requestOptions = {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: this.state.votes_to_skip,
        can_pause: this.state.can_pause,
        room_code: this.props.room_code,
      }),
    };
    fetch("/api/update-room", requestOptions).then((response) => {
      if (response.ok) {
        this.setState({
          success_msg: "Room updated successfully!",
        });
      } else {
        this.setState({
          error_msg: "Error updating room...",
        });
      }
      this.props.updateCallback();
    });
  };

  renderCreateBtns = () => {
    return (
      <Grid container spacing={1} align="center">
        <Grid item xs={12}>
          <Button
            color="primary"
            variant="contained"
            onClick={this.handleCreateRoomBtnClicked}
          >
            Create A Room
          </Button>
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  };

  renderUpdateBtns = () => {
    return (
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={this.handleUpdateBtnClicked}
        >
          Update Room
        </Button>
      </Grid>
    );
  };

  render = () => {
    const title_text = this.props.update ? "Update Room" : "Create a Room";
    return (
      <Grid container spacing={1} align="center">
        <Grid item xs={12}>
          <Collapse
            in={this.state.error_msg != "" || this.state.success_msg != ""}
          >
            {this.state.success_msg != "" ? (
              <Alert
                severity="success"
                onClose={() => {
                  this.setState({ success_msg: "" });
                }}
              >
                {this.state.success_msg}
              </Alert>
            ) : (
              <Alert
                severity="error"
                onClose={() => {
                  this.setState({ error_msg: "" });
                }}
              >
                {this.state.error_msg}
              </Alert>
            )}
          </Collapse>
          <Typography component="h4" variant="h4">
            {title_text}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <FormControl component="fieldset">
            <FormHelperText component="div">
              <div align="center">Guest Control of Playback State</div>
            </FormHelperText>
            <RadioGroup
              row
              defaultValue={this.props.can_pause.toString()}
              onChange={this.handleCanPauseChange}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="Play/Pause"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="No Control"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <FormControl>
            <TextField
              required={true}
              type="number"
              defaultValue={this.state.votes_to_skip}
              onChange={this.handleVotesChange}
              inputProps={{
                min: 1,
                style: { textAlign: "center" },
              }}
            />
            <FormHelperText component="div">
              <div align="center">Votes required to skip song</div>
            </FormHelperText>
          </FormControl>
        </Grid>
        {this.props.update ? this.renderUpdateBtns() : this.renderCreateBtns()}
      </Grid>
    );
  };
}
