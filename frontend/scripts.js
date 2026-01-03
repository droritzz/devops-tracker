// DevOps Tracker Frontend JavaScript
const backendUrl = "http://localhost:8000";

// Router functionality
class Router {
  constructor() {
    this.routes = {
      'home': () => this.showView('home-view'),
      'users': () => this.showView('users-view'),
      'projects': () => this.showView('projects-view'),
      'milestones': () => this.showView('milestones-view')
    };
    
    // Handle browser navigation
    window.addEventListener('popstate', () => this.handleRoute());
    
    // Handle navigation clicks
    document.addEventListener('click', (e) => {
      if (e.target.matches('a[data-route]')) {
        e.preventDefault();
        const route = e.target.getAttribute('data-route');
        this.navigate(route);
      }
    });
  }

  navigate(route) {
    const path = route === 'home' ? '/' : `/${route}`;
    history.pushState(null, '', path);
    this.handleRoute();
  }

  handleRoute() {
    const path = window.location.pathname;
    const route = path === '/' ? 'home' : path.substring(1);
    
    if (this.routes[route]) {
      this.routes[route]();
      this.updateActiveNav(route);
    } else {
      this.routes['home']();
      this.updateActiveNav('home');
    }
  }

  showView(viewId) {
    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
      view.classList.remove('active');
    });
    
    // Show target view
    document.getElementById(viewId).classList.add('active');
  }

  updateActiveNav(route) {
    document.querySelectorAll('.nav a').forEach(link => {
      link.classList.remove('active');
    });
    
    const activeLink = document.querySelector(`[data-route="${route}"]`);
    if (activeLink) {
      activeLink.classList.add('active');
    }
  }
}

// API Service
class ApiService {
  async fetchUsers() {
    try {
      const response = await fetch(`${backendUrl}/users/`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching users:', error);
      return [];
    }
  }

  async createUser(userData) {
    try {
      const response = await fetch(`${backendUrl}/users/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      return await response.json();
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  }

  async fetchProjects() {
    try {
      const response = await fetch(`${backendUrl}/projects/`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching projects:', error);
      return [];
    }
  }

  async createProject(projectData) {
    try {
      const response = await fetch(`${backendUrl}/projects/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(projectData)
      });
      return await response.json();
    } catch (error) {
      console.error('Error creating project:', error);
      throw error;
    }
  }

  async fetchMilestones() {
    try {
      const response = await fetch(`${backendUrl}/milestones/`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching milestones:', error);
      return [];
    }
  }

  async createMilestone(milestoneData) {
    try {
      const response = await fetch(`${backendUrl}/milestones/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(milestoneData)
      });
      return await response.json();
    } catch (error) {
      console.error('Error creating milestone:', error);
      throw error;
    }
  }
}

// App Controller
class AppController {
  constructor() {
    this.router = new Router();
    this.api = new ApiService();
    this.init();
  }

  async init() {
    // Set up form handlers
    this.setupFormHandlers();
    
    // Initial route handling
    this.router.handleRoute();
    
    // Load initial data
    await this.loadAllData();
  }

  setupFormHandlers() {
    // User form
    const userForm = document.getElementById('user-form');
    if (userForm) {
      userForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleUserSubmit();
      });
    }

    // Project form
    const projectForm = document.getElementById('project-form');
    if (projectForm) {
      projectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleProjectSubmit();
      });
    }

    // Milestone form
    const milestoneForm = document.getElementById('milestone-form');
    if (milestoneForm) {
      milestoneForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleMilestoneSubmit();
      });
    }
  }

  async handleUserSubmit() {
    const userData = {
      username: document.getElementById('username').value,
      email: document.getElementById('email').value,
      full_name: document.getElementById('fullName').value || null
    };

    try {
      await this.api.createUser(userData);
      document.getElementById('user-form').reset();
      await this.loadUsers();
      await this.loadProjectOwnerOptions();
      this.showSuccessMessage('User created successfully!');
    } catch (error) {
      this.showErrorMessage('Error creating user. Please try again.');
    }
  }

  async handleProjectSubmit() {
    const ownerId = document.getElementById('projectOwner').value;
    const projectData = {
      name: document.getElementById('projectName').value,
      description: document.getElementById('projectDesc').value || null,
      owner_id: ownerId ? parseInt(ownerId) : null
    };

    try {
      await this.api.createProject(projectData);
      document.getElementById('project-form').reset();
      await this.loadProjects();
      await this.loadProjectOptions();
      this.showSuccessMessage('Project created successfully!');
    } catch (error) {
      this.showErrorMessage('Error creating project. Please try again.');
    }
  }

  async handleMilestoneSubmit() {
    const milestoneData = {
      title: document.getElementById('milestoneTitle').value,
      description: document.getElementById('milestoneDesc').value || null,
      project_id: parseInt(document.getElementById('milestoneProject').value)
    };

    try {
      await this.api.createMilestone(milestoneData);
      document.getElementById('milestone-form').reset();
      await this.loadMilestones();
      this.showSuccessMessage('Milestone created successfully!');
    } catch (error) {
      this.showErrorMessage('Error creating milestone. Please try again.');
    }
  }

  async loadAllData() {
    await Promise.all([
      this.loadUsers(),
      this.loadProjects(),
      this.loadMilestones()
    ]);
    
    await Promise.all([
      this.loadProjectOwnerOptions(),
      this.loadProjectOptions()
    ]);
  }

  async loadUsers() {
    const users = await this.api.fetchUsers();
    const container = document.getElementById('users-list');
    
    if (!container) return;
    
    if (users.length === 0) {
      container.innerHTML = '<p>No users found. Add some users to get started!</p>';
      return;
    }

    container.innerHTML = users.map(user => `
      <div class="item">
        <h4>${user.username}</h4>
        <p><strong>Email:</strong> ${user.email}</p>
        ${user.full_name ? `<p><strong>Full Name:</strong> ${user.full_name}</p>` : ''}
        <p><strong>Created:</strong> ${new Date(user.created_at).toLocaleDateString()}</p>
      </div>
    `).join('');
  }

  async loadProjects() {
    const projects = await this.api.fetchProjects();
    const container = document.getElementById('projects-list');
    
    if (!container) return;
    
    if (projects.length === 0) {
      container.innerHTML = '<p>No projects found. Create your first project!</p>';
      return;
    }

    container.innerHTML = projects.map(project => `
      <div class="item">
        <h4>${project.name}</h4>
        ${project.description ? `<p>${project.description}</p>` : ''}
        <p><strong>Created:</strong> ${new Date(project.created_at).toLocaleDateString()}</p>
      </div>
    `).join('');
  }

  async loadMilestones() {
    const milestones = await this.api.fetchMilestones();
    const container = document.getElementById('milestones-list');
    
    if (!container) return;
    
    if (milestones.length === 0) {
      container.innerHTML = '<p>No milestones found. Add some milestones to track progress!</p>';
      return;
    }

    container.innerHTML = milestones.map(milestone => `
      <div class="item">
        <h4>${milestone.title}</h4>
        ${milestone.description ? `<p>${milestone.description}</p>` : ''}
        <p><strong>Status:</strong> ${milestone.status || 'Todo'}</p>
        <p><strong>Project ID:</strong> ${milestone.project_id}</p>
        <p><strong>Created:</strong> ${new Date(milestone.created_at).toLocaleDateString()}</p>
      </div>
    `).join('');
  }

  async loadProjectOwnerOptions() {
    const users = await this.api.fetchUsers();
    const select = document.getElementById('projectOwner');
    
    if (!select) return;
    
    select.innerHTML = '<option value="">Select Owner</option>' +
      users.map(user => `<option value="${user.id}">${user.username} (${user.email})</option>`).join('');
  }

  async loadProjectOptions() {
    const projects = await this.api.fetchProjects();
    const select = document.getElementById('milestoneProject');
    
    if (!select) return;
    
    select.innerHTML = '<option value="">Select Project</option>' +
      projects.map(project => `<option value="${project.id}">${project.name}</option>`).join('');
  }

  showSuccessMessage(message) {
    this.showMessage(message, 'success');
  }

  showErrorMessage(message) {
    this.showMessage(message, 'error');
  }

  showMessage(message, type) {
    // Remove any existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());

    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 1rem;
      border-radius: 4px;
      color: white;
      background-color: ${type === 'success' ? '#27ae60' : '#e74c3c'};
      z-index: 1000;
      max-width: 300px;
    `;
    messageDiv.textContent = message;

    document.body.appendChild(messageDiv);

    // Auto-remove after 3 seconds
    setTimeout(() => {
      if (messageDiv.parentNode) {
        messageDiv.parentNode.removeChild(messageDiv);
      }
    }, 3000);
  }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new AppController();
});
