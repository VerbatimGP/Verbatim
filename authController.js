

const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const JWT_SECRET = 'your_jwt_secret_key'; 


exports.signup = async (req, res) => {
    const { name, email, password, confirmPassword, role } = req.body;

    
    if (password !== confirmPassword) {
        return res.status(400).json({ message: 'Passwords do not match' });
    }

   
    const existingUser = await User.findOne({ email });
    if (existingUser) {
        return res.status(400).json({ message: 'User already exists' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    
    const newUser = new User({ name, email, password: hashedPassword, role });
    
    try {
        await newUser.save();
        res.status(201).json({ message: 'User created successfully' });
    } catch (error) {
        res.status(400).json({ error: 'Error creating user' });
    }
};


exports.login = async (req, res) => {
    const { email, password } = req.body;
    
    const user = await User.findOne({ email });
    if (!user || !(await bcrypt.compare(password, user.password))) {
        return res.status(401).json({ message: 'Invalid credentials' });
    }

    const token = jwt.sign({ id: user._id }, JWT_SECRET);
    
    
    if (user.role === 'student') {
        return res.json({ token, redirectUrl: '/student/dashboard' }); 
    } else if (user.role === 'faculty') {
        return res.json({ token, redirectUrl: '/faculty/dashboard' }); 
    }
};

// Request password reset function
exports.requestPasswordReset = async (req, res) => {
    const { email } = req.body;
    
    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ message: 'User not found' });

   
    
    res.status(200).json({ message: 'Email verified. Now provide your new password.' });
};

// Update password function
exports.updatePassword = async (req, res) => {
    const { email, newPassword } = req.body;

    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ message: 'User not found' });

   t
    const hashedPassword = await bcrypt.hash(newPassword, 10);
    
    user.password = hashedPassword;
    
    try {
        await user.save();
        res.status(200).json({ message: 'Password updated successfully' });
    } catch (error) {
        res.status(400).json({ error: 'Error updating password' });
    }
};