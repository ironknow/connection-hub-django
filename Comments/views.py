from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404

from Comments.models import Comment
from Posts.models import Post


@login_required(login_url='user-login')
def comments(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if ('comment' not in request.POST) or (not bool(request.POST['comment'])):
            response = JsonResponse(
                data={
                    'success': False,
                    'error': 'Comment is required'
                }
            )
            response.status_code = 400
            return response

        comment = request.POST['comment']
        comment = post.comments.create(user=request.user, content=comment)
        post.comments_count += 1
        post.save()
        return JsonResponse(
            data={
                'success': True,
                'comment': comment.get_context(),
            }
        )
    return JsonResponse(
        data={
            'success': True,
            'comments': [
                comment.get_context()
                for comment in post.comments.all()
            ],
        }
    )


@login_required(login_url='user-login')
def delete_comment(request: HttpRequest, comment_id: int):
    comment = get_object_or_404(Comment.admin_objects, id=comment_id)
    if not comment.user.id == request.user.id:
        return JsonResponse(
            data={
                'success': False,
                'error': 'Not authorized person'
            },
            status=403
        )

    comment.delete()
    return JsonResponse(
        data={
            'success': True
        }
    )
