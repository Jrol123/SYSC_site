from django.db import models


class Block(models.Model):
    block_type = models.ForeignKey("SHC.BlockType",
                                   on_delete=models.CASCADE)
    name = models.CharField("Название", max_length=200)
    text = models.TextField("Основной текст")


class BlockLink(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    doc = models.ForeignKey("documents.Doc", on_delete=models.CASCADE)


class BlockForm(models.Model):
    empty = models.TextField("хммммммммммммммммммммммммммммммммммммммм")


class BlockType(models.Model):
    form = models.ForeignKey(BlockForm, on_delete=models.CASCADE)
    border_color = models.CharField("Цвет границы", max_length=50)
    fill_color = models.CharField("Цвет заливки", max_length=50)


class BlockConnection(models.Model):
    connect_type = models.ForeignKey("SHC.ConnectionType",
                                     on_delete=models.CASCADE)
    main_block = models.ForeignKey(Block, on_delete=models.CASCADE,
                                   verbose_name="Главный блок",
                                   related_name="main_block")
    side_block = models.ForeignKey(Block, on_delete=models.CASCADE,
                                   verbose_name="Побочный блок",
                                   related_name="side_block")
    color = models.CharField("Цвет", max_length=50)


class ConnectionType(models.Model):
    empty = models.TextField("пжпжпжпжппжпжпжпжпжпжппжпжпжпжпжпжпжпжпж")
