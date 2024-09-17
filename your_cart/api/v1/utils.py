from your_cart.models import Cart

def get_cart(request):
    if request.user.is_authenticated:
        # Authenticated user, retrieve or create cart linked to user
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Guest user, retrieve or create cart linked to session ID
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    return cart