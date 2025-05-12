from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def get_hello():
    """
    Simple hello endpoint equivalent to the Spring Boot AppController
    """
    return "hello"