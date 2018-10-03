import random, time

from celery.exceptions import SoftTimeLimitExceeded

from src import celery, app
from src.libs import CouponSpiders
from src.models import Store, Coupon, db, session, StoreStatus

@celery.task(bind=True, time_limit=600, soft_time_limit=550)
def check_store(self, id):
    with app.app_context():
        store = Store.query.get(id)
        store.status = StoreStatus.working

        try:
            session.commit()
        except Exception as e:
            print(str(e))
            session.rollback()

        source = store.source
        spider = CouponSpiders[source.name.lower()](self, base_url=source.base_url, start_point=store.start_point)
        result = spider.run(id)
        
        return {'current': 50, 'total': 50, 'status': 'Job is Completed!', 'result': result}


@celery.task(bind=True)
def grab_coupons(self):
    with app.app_context():
        # Removing all of the current coupons
        Coupon.query.delete()
        try:
            session.commit()
        except Exception as e:
            print(str(e))
            session.rollback()

        print("===================================================")
        print("+++++++++     Starting the scheduler    +++++++++++")
        print("---------------------------------------------------")

        count = 0

        for store in Store.query.all():
            if not store.source:# or store.source.name != 'offers': #!= 'retailmenot': #'groupon':
                continue

            # if count > 3:
            #     break
            # else:
            #     count += 1
            
            task = check_store.apply_async([store.id])
            store.job_uid = task.id
            store.status = StoreStatus.pending

            # Should be removed in production mode.
            # break
        
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print(str(e))


