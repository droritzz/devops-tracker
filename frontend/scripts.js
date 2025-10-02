const API_URL = "http://localhost:8000";

// --- Users ---
async function createUser() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;

    const res = await fetch(`${API_URL}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email })
    });
    const data = await res.json();
    console.log(data);
    listUsers();
}

async function listUsers() {
    const res = await fetch(`${API_URL}/users/`);
    const users = await res.json();
    const ul = document.getElementById("usersList");
    ul.innerHTML = "";
    users.forEach(u => {
        const li = document.createElement("li");
        li.textContent = `${u.id}: ${u.username} (${u.email})`;
        ul.appendChild(li);
    });
}

// --- Projects ---
async function createProject() {
    const name = document.getElementById("projectName").value;
    const description = document.getElementById("projectDescription").value;

    const res = await fetch(`${API_URL}/projects/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
    });
    const data = await res.json();
    console.log(data);
    listProjects();
}

async function listProjects() {
    const res = await fetch(`${API_URL}/projects/`);
    const projects = await res.json();
    const ul = document.getElementById("projectsList");
    ul.innerHTML = "";
    projects.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `${p.id}: ${p.name} - ${p.description}`;
        ul.appendChild(li);
    });
}

// --- Milestones ---
async function createMilestone() {
    const title = document.getElementById("milestoneTitle").value;
    const project_id = document.getElementById("milestoneProjectId").value;

    const res = await fetch(`${API_URL}/milestones/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, project_id })
    });
    const data = await res.json();
    console.log(data);
    listMilestones();
}

async function listMilestones() {
    const res = await fetch(`${API_URL}/milestones/`);
    const milestones = await res.json();
    const ul = document.getElementById("milestonesList");
    ul.innerHTML = "";
    milestones.forEach(m => {
        const li = document.createElement("li");
        li.textContent = `${m.id}: ${m.title} (Project ${m.project_id})`;
        ul.appendChild(li);
    });
}

// Load data on page load
listUsers();
listProjects();
listMilestones();
