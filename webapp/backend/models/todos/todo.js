// TODO: Convert code in this file over to NSMQ AI database models

const mongoose = require('mongoose');

const Todo = mongoose.model('Todo', {
    text : {
        type: String,
        trim: true,
        required: true
    }
});

module.exports = {Todo};
