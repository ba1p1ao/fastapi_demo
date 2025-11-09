from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.posts import PostCreate, PostDeleteResponse, PostResponse, PostUpdate
from models.models import User, Post
from core.dependencies import get_current_user

router_post = APIRouter()


@router_post.get("/posts", response_model=List[PostResponse])
async def getAllPosts():
    """获取所有posts数据"""
    posts = await Post.all().prefetch_related("author")
    posts_response = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "author_name": post.author.username,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
        posts_response.append(PostResponse(**post_dict))

    return posts_response


@router_post.post("/posts", response_model=PostResponse)
async def createPost(
    post_data: PostCreate, current_user: User = Depends(get_current_user)
):
    """
    创建新文章
    - 需要认证
    - 当前用户自动设置为文章作者
    """
    print(post_data)
    post = await Post.create(
        title=post_data.title,
        content=post_data.content,
        author=current_user,
    )
    await post.fetch_related("author")
    post_dict = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "author_name": post.author.username,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }

    return PostResponse(**post_dict)


@router_post.put("/posts/{post_id}", response_model=PostResponse)
async def updatePost(
    post_id: int, post_data: PostUpdate, current_user: User = Depends(get_current_user)
):
    post = await Post.filter(id=post_id).prefetch_related("author").first()
    print(post_data)
    if not post:
        raise HTTPException(status_code=404, detail="文章没有找到")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权更新此文章")
    # 更新文章
    post.title = post_data.title
    post.content = post_data.content
    await post.save()

    # 更新时间
    await post.refresh_from_db()

    post_dict = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "author_name": post.author.username,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }

    return PostResponse(**post_dict)


@router_post.delete("/posts/{post_id}")
async def deletePost(post_id: int, current_user: User = Depends(get_current_user)):
    post = await Post.filter(id=post_id).prefetch_related("author").first()
    if not post:
        raise HTTPException(status_code=404, detail="文章没有找到")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权更新此文章")

    await post.delete()
    
    return PostDeleteResponse(
        message="文章删除成功",
        post_id=post_id
    )
