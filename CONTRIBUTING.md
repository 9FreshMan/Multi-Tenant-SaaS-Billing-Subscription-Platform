# Contributing to Multi-Tenant SaaS Billing Platform

First off, thank you for considering contributing to this project! 🎉

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Be kind to others.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** and description
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, Node version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **Include mockups or examples** if applicable

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write clear commit messages
6. Update documentation if needed

## Development Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Running Tests

```bash
# Backend
cd backend
pytest tests/ -v --cov=app

# Frontend
cd frontend
npm test
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Use Ruff for linting: `ruff check .`
- Format with Black: `black .`
- Maximum line length: 100 characters

Example:
```python
from typing import Optional

async def get_user(user_id: str) -> Optional[User]:
    """
    Retrieve a user by ID.
    
    Args:
        user_id: The unique identifier of the user
        
    Returns:
        User object if found, None otherwise
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow React best practices
- Use functional components with hooks
- Use ESLint: `npm run lint`
- Format with Prettier: `npm run format`

Example:
```typescript
interface User {
    id: string;
    email: string;
    fullName: string;
}

export const UserCard: React.FC<{ user: User }> = ({ user }) => {
    return (
        <div className="rounded-lg border p-4">
            <h3>{user.fullName}</h3>
            <p>{user.email}</p>
        </div>
    );
};
```

## Commit Messages

Use clear and meaningful commit messages:

- `feat: add user invitation feature`
- `fix: resolve stripe webhook timeout`
- `docs: update API documentation`
- `test: add tests for subscription service`
- `refactor: simplify tenant middleware`
- `chore: update dependencies`

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Core configurations
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── tasks/        # Celery tasks
│   └── tests/            # Backend tests
│
└── frontend/
    ├── src/
    │   ├── components/   # Reusable components
    │   ├── pages/        # Page components
    │   ├── services/     # API services
    │   └── hooks/        # Custom hooks
    └── tests/            # Frontend tests
```

## Testing Guidelines

### Backend Tests

- Write tests for all new endpoints
- Test both success and error cases
- Mock external services (Stripe, email)
- Use pytest fixtures for common setup

```python
def test_create_subscription(client, db_session, mock_stripe):
    response = client.post("/api/v1/subscriptions/", json={
        "plan_id": "plan_123",
        "payment_method_id": "pm_123"
    })
    assert response.status_code == 201
    assert response.json()["status"] == "active"
```

### Frontend Tests

- Test component rendering
- Test user interactions
- Test API integration
- Use React Testing Library

```typescript
test('renders user profile', () => {
    render(<UserProfile user={mockUser} />);
    expect(screen.getByText(mockUser.fullName)).toBeInTheDocument();
});
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🚀
