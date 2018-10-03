"""
Initializing routes for Coupons app
"""

from .views import CouponsView, CouponView

def init_routes(app):
    app.add_url_rule('/', view_func=CouponsView.as_view('index'))
    app.add_url_rule('/<int:id>', view_func=CouponView.as_view('show'))

if __name__ == "__main__":
    print("Something went wrong...")
