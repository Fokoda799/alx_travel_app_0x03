# ALX Travel App - API Development

## Project Overview
This project is a Django REST Framework-based backend for a travel booking platform similar to Airbnb. It provides RESTful API endpoints for managing property listings, bookings, and reviews.

## Milestones Completed

### ✅ Milestone 1: Setup and Database Configuration
- Configured PostgreSQL database
- Set up Django project structure
- Configured environment variables

### ✅ Milestone 2: Creating Models, Serializers, and Seeders
- Created custom user model with email authentication
- Implemented core models: Listing, Booking, Review
- Built serializers with nested relationships
- Added data validation at both model and serializer levels

### ✅ Milestone 3: Creating Views and API Endpoints
- Implemented ViewSets for CRUD operations
- Configured automatic URL routing
- Set up RESTful API endpoints

---

## Project Structure

```
alx_travel_app/
├── listings/
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API ViewSets
│   └── urls.py            # URL routing
├── alx_travel_app/
│   ├── settings.py        # Project settings
│   └── urls.py            # Main URL configuration
└── manage.py
```

---

## Models

### CustomUser
Custom user model using email for authentication.

**Fields:**
- `email` (unique, used for login)
- `username`
- `phone_number`
- `profile_image`

### Listing
Represents a property available for booking.

**Fields:**
- `host` (ForeignKey to CustomUser)
- `name`
- `description`
- `location`
- `price_per_night`
- `is_available`

### Booking
Represents a user's reservation of a listing.

**Fields:**
- `property` (ForeignKey to Listing)
- `user` (ForeignKey to CustomUser)
- `start_date`
- `end_date`
- `total_price`
- `status` (PENDING, CONFIRMED, CANCELLED)

**Validation:**
- End date must be after start date
- Start date cannot be in the past
- Check-in and check-out cannot be on the same day

### Review
User feedback on a listing.

**Fields:**
- `property` (ForeignKey to Listing)
- `user` (ForeignKey to CustomUser)
- `rating`
- `comment`

---

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

### Listings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/listings/` | List all listings |
| POST | `/api/listings/` | Create a new listing |
| GET | `/api/listings/{id}/` | Retrieve a specific listing |
| PUT | `/api/listings/{id}/` | Update a listing (full) |
| PATCH | `/api/listings/{id}/` | Update a listing (partial) |
| DELETE | `/api/listings/{id}/` | Delete a listing |

### Bookings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings/` | List all bookings |
| POST | `/api/bookings/` | Create a new booking |
| GET | `/api/bookings/{id}/` | Retrieve a specific booking |
| PUT | `/api/bookings/{id}/` | Update a booking (full) |
| PATCH | `/api/bookings/{id}/` | Update a booking (partial) |
| DELETE | `/api/bookings/{id}/` | Delete a booking |

### Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reviews/` | List all reviews |
| POST | `/api/reviews/` | Create a new review |
| GET | `/api/reviews/{id}/` | Retrieve a specific review |
| PUT | `/api/reviews/{id}/` | Update a review (full) |
| PATCH | `/api/reviews/{id}/` | Update a review (partial) |
| DELETE | `/api/reviews/{id}/` | Delete a review |

---

## Key Features Implemented

### 1. ViewSets
Used Django REST Framework's `ModelViewSet` to automatically handle all CRUD operations without writing separate view functions.

**Benefits:**
- Less boilerplate code
- Consistent API behavior
- Automatic handling of HTTP methods

### 2. Nested Serializers
Implemented nested serializers to show related data in API responses.

**Example Response:**
```json
{
  "id": 1,
  "host": {
    "id": 5,
    "email": "john@example.com",
    "username": "john"
  },
  "name": "Beach House",
  "location": "Miami, FL",
  "price_per_night": "150.00",
  "is_available": true
}
```

Instead of just showing `"host": 5`, the API returns complete host information.

### 3. Automatic URL Routing
Used DRF's `DefaultRouter` to automatically generate URL patterns.

**Benefits:**
- Reduced manual URL configuration (from 12+ patterns to 3 lines)
- RESTful URL structure by default
- Easy to add new endpoints

### 4. Data Validation
Implemented validation at two levels:

**Serializer Level (`validate()` method):**
- Runs when data comes through the API
- Returns user-friendly error messages in JSON format

**Model Level (`clean()` method):**
- Runs when data is saved through Django Admin or direct model operations
- Provides a safety net for data integrity

---

## How to Run

### 1. Install Dependencies
```bash
pip install django djangorestframework psycopg2-binary
```

### 2. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Run the Development Server
```bash
python manage.py runserver
```

### 5. Access the API
- Browsable API: `http://127.0.0.1:8000/api/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

---

## Testing the API

### Using Browser (Browsable API)
Django REST Framework provides a web interface for testing:
1. Navigate to `http://127.0.0.1:8000/api/listings/`
2. Use the HTML forms to create, view, update, and delete records
3. View JSON responses directly in the browser

### Using Postman (Recommended)
**Create a Listing:**
```
POST http://127.0.0.1:8000/api/listings/
Content-Type: application/json

{
  "host": 1,
  "name": "Cozy Beach House",
  "description": "Beautiful beach house with ocean view",
  "location": "Miami, FL",
  "price_per_night": "150.00",
  "is_available": true
}
```

**Get All Listings:**
```
GET http://127.0.0.1:8000/api/listings/
```

**Get a Specific Listing:**
```
GET http://127.0.0.1:8000/api/listings/1/
```

**Update a Listing:**
```
PUT http://127.0.0.1:8000/api/listings/1/
Content-Type: application/json

{
  "host": 1,
  "name": "Updated Beach House Name",
  "description": "Updated description",
  "location": "Miami, FL",
  "price_per_night": "200.00",
  "is_available": true
}
```

**Delete a Listing:**
```
DELETE http://127.0.0.1:8000/api/listings/1/
```

---

## Technical Concepts Explained

### What is a ViewSet?
A ViewSet is a class that handles multiple related operations (list, create, retrieve, update, delete) in one place. Instead of writing 5 separate view functions, you write one ViewSet class.

### What is a Router?
A Router automatically generates URL patterns for your ViewSets. It follows REST conventions to create URLs like:
- `/api/listings/` for listing and creating
- `/api/listings/5/` for retrieving, updating, and deleting

### Why Nested Serializers?
When you fetch a listing, it's more useful to see the host's name and email rather than just `"host": 5`. Nested serializers automatically include related object details in the response.

### Why read_only=True?
Setting nested fields as `read_only=True` means:
- ✅ They appear in GET responses
- ❌ They cannot be set via POST/PUT requests
- 🔒 This prevents security issues where users might try to set foreign keys to values they shouldn't access

---

## Known Limitations & Future Improvements

### Current Limitations:
1. **No Authentication**: Anyone can access and modify all data
2. **No Permission Controls**: Users can modify other users' listings
3. **No Automatic Host Assignment**: When creating a listing, the host must be manually specified
4. **No Swagger Documentation**: API endpoints are not yet documented with Swagger

### Planned Improvements:
1. Add authentication (JWT or Token-based)
2. Implement permission classes to restrict access
3. Automatically assign the logged-in user as the host when creating listings
4. Add Swagger/OpenAPI documentation
5. Add filtering and search capabilities
6. Implement pagination for large datasets

---

## Common Issues & Solutions

### Issue: "host field is required" when creating a listing
**Cause:** The host field is marked as read_only in the serializer but is required in the model.

**Temporary Solution:** Include the host ID in your POST request.

**Proper Solution (Coming Soon):** Implement authentication and automatically assign the logged-in user as the host.

### Issue: "End date must be after start date" error
**Cause:** Your booking has the same or earlier end_date than start_date.

**Solution:** Ensure end_date is at least one day after start_date.

---

## Learning Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Django Official Documentation](https://docs.djangoproject.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

## Author
ALX Software Engineering Program - Backend Specialization

## License
This project is for educational purposes.
