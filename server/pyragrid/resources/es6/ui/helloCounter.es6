//TODO envelop with umd

class ShowNumber extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    let {number} = this.props;

    return (
      <span>{number}</span>
    );
  }
}

let autoUpdateFromServer = true;

// TODO rewrite
// TODO add hello world line with server time and user name
// TODO refer to component data from store by component id

class HelloCounter extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    let {store} = this.props;

    return (
      <div>
        <button onClick={ event => {
          store.data.number = store.data.number - 1;
        } }>-</button>&nbsp;
        <ShowNumber number={store.data.number} />&nbsp;
        <button onClick={ event => {
          store.data.number = store.data.number + 1;
        } }>+</button>&nbsp;
        <p>updates from server: {store.data.serverTime}</p>
        <button onClick={ event => {
          autoUpdateFromServer = !autoUpdateFromServer;
        }}>Toggle autoupdate from server</button>
      </div>
    );
  }
}