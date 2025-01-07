from django.contrib import admin
from unfold.sites import UnfoldAdminSite
from unfold.admin import ModelAdmin
from .models import Tenant, Domain

class TenantAdminSite(UnfoldAdminSite):
    settings_name = "UNFOLD_TENANT"


tenant_admin_site = TenantAdminSite(name="tenant_admin")

@admin.register(Tenant, site=tenant_admin_site)
class TenantAdmin(ModelAdmin):
    model = Tenant

@admin.register(Domain, site=tenant_admin_site)
class DomainAdmin(ModelAdmin):
    model = Domain