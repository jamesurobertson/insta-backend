@bp.route('', methods= ["POST"])
def postComment():
    data = request.json
    print(data)
    content = Comment(user_id=data['userId'], post_id=data['postId'], content=data['content'])
    db.session.add(content)
    db.session.commit()

    return content.to_dict()
