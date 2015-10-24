from mod_python import apache
import HiveRouter

def go(req):
    router = HiveRouter.HiveRouter.factory(req)
    
    status, output = router.output()

    req.write(output)

    return status


