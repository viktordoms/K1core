from django.contrib import admin

from core.models import UserCredentials, ExternalCredentials, Currency, Provider, Block


class UserCredentialsAdmin(admin.ModelAdmin):
    list_display = ("user", "expired_at")

admin.site.register(UserCredentials, UserCredentialsAdmin)


class ExternalCredentialsAdmin(admin.ModelAdmin):
    list_display = ("code", "api_key", "access_token", "test_mode", "base_url", "provider")

admin.site.register(ExternalCredentials, ExternalCredentialsAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name")

admin.site.register(Currency, CurrencyAdmin)


class ProviderAdmin(admin.ModelAdmin):
    list_display = ("code", "name",)

admin.site.register(Provider, ProviderAdmin)


class BlockAdmin(admin.ModelAdmin):
    list_display = ("currency", "provider", "block_numbers", "created_at", "stored_at")

admin.site.register(Block, BlockAdmin)