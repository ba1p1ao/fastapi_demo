from fastapi import APIRouter, Depends
from typing import List
from tortoise.expressions import Q
from models.movie import Movie
from models.movie_category import MovieCategories
from models.category import Category
from models.comment import Comment
from models.user import User
from schemas.movie import MovieList
from core import deps

router = APIRouter()


@router.get("/", response_model=MovieList)
async def getAllMoives(
    page: int = 1,
    size: int = 20,
    category: str = None,
    search: str = None,
    order_by: str = "id",
    order: str = "asc",
):
    skip = (page - 1) * size
    order_prefix = "" if order == "asc" else "-"
    category_filter = {}

    if category is not None:
        category_filter = {"movie_categories__category__id": category}
        movies = (
            await Movie.filter(**category_filter)
            .order_by(f"{order_prefix}{order_by}")
            .offset(skip)
            .limit(size)
        )

    elif search is not None:
        movies = (
            await Movie.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(director__icontains=search)
                | Q(actors__icontains=search)
                | Q(plot__icontains=search)
            )
            .order_by(f"{order_prefix}{order_by}")
            .offset(skip)
            .limit(size)
        )
    else:
        movies = (
            await Movie.all()
            .order_by(f"{order_prefix}{order_by}")
            .offset(skip)
            .limit(size)
        )

    response_data = {
        "total": len(movies),
        "page": page,
        "size": size,
        "movies": [],
    }
    for movie in movies:
        response_data["movies"].append(
            {
                "id": movie.id,
                "title": movie.title,
                "cover_url": movie.cover_url,
                "description": movie.description,
                "release_year": movie.release_year,
                "rating": movie.rating,
                "director": movie.director,
            }
        )
    return response_data


@router.get("/{movie_id}")
async def getMovieDetail(movie_id: int):

    movie = await Movie.filter(id=movie_id).first()
    # print(dict(movie))

    # select categories.name
    # from categories
    # left join movie_categories on categories.id = movie_categories.category_id
    # left join movies on movies.id = movie_categories.movie_id
    # where movies.id = 1;
    categories = await Category.filter(
        movie_categories__movie__id=movie.id
    ).values_list("name", flat=True)

    # print(categories)
    comments = await Comment.filter(
        movie_id=movie.id, is_deleted=False
    ).prefetch_related("user")

    new_comments = []
    for comment in comments:
        new_comments.append(
            {
                "avatar_url": comment.user.avatar_url,
                "username": comment.user.username,
                "content": comment.content,
                "rating": float(comment.rating) if comment.rating is not None else None,
                "created_at": comment.created_at,
            }
        )

    response_data = {
        "categories": [{"name": name} for name in categories],
        "comments": new_comments,
        **dict(movie),
    }
    return response_data
