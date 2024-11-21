const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

// Initialize Express app
const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());

// MongoDB connection
mongoose.connect('mongodb://127.0.0.1:27017/carsDB', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Connected to MongoDB'))
    .catch((err) => console.error('MongoDB connection error:', err));

// Car schema and model
const carSchema = new mongoose.Schema({
    name: { type: String, required: true },
    details: { type: String, required: true }
});

const Car = mongoose.model('Car', carSchema);

// Routes
// Add a car
app.post('/cars', async (req, res) => {
    try {
        const { name, details } = req.body;
        const car = new Car({ name, details });
        await car.save();
        res.status(201).json({ message: 'Car added successfully!', car });
    } catch (err) {
        res.status(500).json({ message: 'Error adding car', error: err.message });
    }
});

// Get car details by name
app.get('/cars/:name', async (req, res) => {
    try {
        const carName = req.params.name;
        const car = await Car.findOne({ name: carName });
        if (!car) return res.status(404).json({ message: 'Car not found' });
        res.status(200).json(car);
    } catch (err) {
        res.status(500).json({ message: 'Error fetching car', error: err.message });
    }
});

// Start server
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));