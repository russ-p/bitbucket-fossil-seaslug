

def get_instance_by_classname(classname, *arg, **kvarg):
    module_name, class_name = classname.rsplit ('.',1)
    imported_module_object = __import__(module_name, fromlist=[class_name,])
    kls = getattr(imported_module_object, class_name)
    return kls(*arg, **kvarg)

ru = lambda text:text.decode("utf-8")
ur = lambda text:text.encode("utf-8")

def explore (filename):
    from settings import DATA_DIR
    import os
    return os.path.join (DATA_DIR, filename)
    
def admin_only(fn):
    def wrapper (plugin, msg, *arg):
        from settings import ADMINS
        if msg.sender.id in ADMINS:
            fn(msd, *arg)
        else:
            msg.send_response(u'No! U R NOT ADMIN!')
    return wrapper
