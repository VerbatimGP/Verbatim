

const express = require('express');
const { signup, login, requestPasswordReset, updatePassword } = require('../controllers/authController');

const router = express.Router();

router.post('/signup', signup);                    
router.post('/login', login);                      
router.post('/request-password-reset', requestPasswordReset); 
router.post('/update-password', updatePassword);    

module.exports = router;