export default {
  maxSize: 15,
  state: {
    path: []
  },
  addHistory(path) {
    // simple queue ;)
    if (this.state.path.length > this.maxSize) {
      this.state.path.shift()
    }
    this.state.path.push(path)
  },
  getHistory() {
    return this.state.path
  }
}
