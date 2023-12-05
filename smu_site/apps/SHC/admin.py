from django.contrib import admin
from .models import (Block, BlockType, BlockLink,
                    BlockForm, BlockConnection, ConnectionType)


admin.site.register(Block)
admin.site.register(BlockType)
admin.site.register(BlockLink)
admin.site.register(BlockForm)
admin.site.register(BlockConnection)
admin.site.register(ConnectionType)
