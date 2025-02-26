# DevReady  

**AI-Powered Coding Interview Prep Platform**  

DevReady is an **interactive coding interview preparation tool** designed *by CS students, for CS students.* It provides **personalized coding challenges, real-time AI feedback, and mock interviews** to help candidates master problem-solving skills with structured, step-by-step learning.  

---

## 🚀 Features  

- **Interactive Coding Challenges** – Real-world tasks tailored for technical interviews.  
- **AI-Powered Feedback** – Get instant, personalized insights and code analysis.  
- **Mock Interviews** – Simulated coding and behavioral interviews with AI.  
- **Step-by-Step Learning** – Focus on *how* to solve problems, not just the final answer.  
- **Performance Tracking** – Analyze strengths and weaknesses to improve.  

---

## 🛠 Tech Stack  

### **Frontend:**  
- **Bootstrap** for styling and responsiveness  
- **JavaScript** for interactive elements and real-time updates  
- **Code Execution Tools** (to compile and run submitted code in various languages)  

### **Backend:**  
- **Flask** (Python) as the web framework  
- **Virtual Environment** for dependency management  
- **MySQL** as the relational database for storing user data, solutions, and performance metrics  

### **APIs & AI Models:**  
- **OpenAI GPT-4o Mini** for code analysis and personalized feedback  

---

## 📦 Installation  

### **1. Clone the repository:**  
```bash
git clone https://github.com/your-username/devready.git
cd devready
```

### **2. Set up the virtual environment:**  
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install dependencies:**  
```bash
pip install -r requirements.txt
```

### **4. Set up MySQL database:**  
- Install MySQL and create a new database:  
  ```sql
  CREATE DATABASE devready_db;
  ```
- Update `config.py` with your database credentials.  

### **5. Run the Flask backend:**  
```bash
flask run
```

### **6. Open the frontend in your browser**  
Once the Flask server is running, access the app at:  
```
http://127.0.0.1:5000
```

---

## 🤝 Contributing  

We welcome contributions! Feel free to submit issues, pull requests, or suggest improvements.  

### Steps to Contribute:  

1. Fork the repo and create a new branch.  
2. Make your changes and commit with a clear message.  
3. Open a pull request for review.  

---

## 📜 License  

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.  
See [LICENSE](LICENSE) for details.  

---

## 📬 Contact  

Have questions or feedback? Reach out to us:  

- **GitHub:** [DevReady](https://github.com/tvtusc25/devready)
