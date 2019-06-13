// index.js


module.exports = () => {

  const data = { posts: [], users: [], comments: [], todos: [] }


  // Create 100 users
  for (let i = 0; i < 100; i++) {
    data.users.push({ id: i + 1, name: `user${i + 1}`, username: `user_name${i + 1}`, email: `user${i + 1}@test.com` })
  }


  // Create 100 posts
  for (let i = 0; i < 100; i++) {
    data.posts.push({ id: i + 1, title: `post ${i + 1}`, body: `Hello This is a post ${i + 1}`, userId: data.users[i].id })
  }


  //Create 1000 comments

  var comId = 0
  var n

  for (let i = 0; i < 100; i++){
    n = 0
    while(n != 10) {
        n++;
        comId ++;
        data.comments.push({ id: comId, postId: i + 1, name: `Test comment-${comId}`, email: data.users[i].email, body: `Hello There. Hello to User ${data.users[i].email}` })
    }
    //data.comments.push({ id: i, postId: i, name: `Test comment-${i}`, email: data.users[i].email, body: `Hello There. Hello to User ${data.users[i].email}` })
  }


  // Create 200 todos
  var todoId = 0
  var t

  for (let i = 1; i < 100 + 1; i++){
    t = 1
    while(t != 3){
        t++;
        todoId ++;
        data.todos.push({ id: todoId, userId: i, title: `Task ${todoId}`, completed: true })
    }
  }

  return data
}
