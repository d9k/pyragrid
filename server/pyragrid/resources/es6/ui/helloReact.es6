class HelloReact extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    let {appealTo, serverTime} = this.props;

    // if (!id){
    //   throw "id not defined";
    // }

    return (
      <div>
        Hello, {appealTo}! Time at server is: {serverTime}
      </div>
    );
  }
}