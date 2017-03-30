var lunr = require('./node_modules/lunr/lunr.js'),
fs = require('fs')

var idx = lunr(function () {
  this.ref('id')

  this.field('title', { boost: 10 })
  this.field('tags', { boost: 100 })
  this.field('body')
})

fs.readFile('example_data2.json', function (err, data) {
  if (err) throw err

  var raw = JSON.parse(data)

  var questions = raw.questions.map(function (q) {
    return {
      id: q.question_id,
      title: q.title,
      body: q.body,
      tags: q.tags.join(' ')
    }
  })

  questions.forEach(function (question) {
    idx.add(question)
  })


  fs.writeFile('index.json', JSON.stringify(idx), function (err) {
    if (err) throw err
    console.log('done')

  })
})
