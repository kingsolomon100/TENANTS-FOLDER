def convert_tenant(tenant: dict)->dict:
    if not tenant:
        return None 
    
    created_at = tenant.get('created_at')
    created_at_str = (created_at.strftime("%d-%b-%Y, %I:%M%p") if created_at else None)

    updated_time = tenant.get('updated_at')
    updated_time_str = (updated_time.strftime("%d-%b-%Y, %I:%M%p ") if updated_time else None)


    return {
        "id": str(tenant["_id"]), 
        "roomNumber": tenant.get('roomNumber'), 
        "name": tenant.get('name'), 
        "email":  tenant.get('email'),
        "gender": tenant.get('gender'), 
        "created_at": created_at_str, 
        "updated_time": updated_time_str
    }

def convert_tenants(tenants: list)->list:
    if not tenants:
        return []
    
    return [convert_tenant(tenant) for tenant in tenants if tenant] 
    
