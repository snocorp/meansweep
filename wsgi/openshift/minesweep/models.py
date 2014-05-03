from django.db import models

# Field
# width - width of the grids
# height - height of the grids
# count - the number of bombs on the field
# active - whether the game is stil in progress or not
# created_date - the date the field was created
class Field(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    count = models.IntegerField()
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField('date created')
    
    def __unicode__(self):
        if self.active:
            return 'Field(' + str(self.width) + 'x' + str(self.height) + ', ' + str(self.count) + ' bombs)'
        else:
            return 'Field(' + str(self.width) + 'x' + str(self.height) + ', game over)'

# Grid
# x - 0-based horizontal position of the grid from the left of the field
# y - 0-based vertical position of the grid from the top of the field
# value - -1 indicates a bomb, 0-8 indicates number of neighbours with bombs
# flagged - indicates a grid has been flagged as hacing a bomb
# swept - indicates a grid has been cleared (or exploded)
class Grid(models.Model):
    field = models.ForeignKey(Field)
    x = models.IntegerField()
    y = models.IntegerField()
    value = models.IntegerField()
    flagged = models.BooleanField(default=False)
    swept = models.BooleanField(default=False)
    
    def __unicode__(self):
        val = self.value
        if self.value == -1:
            val = '!'
            
        clear = '?'
        if self.flagged:
            clear = '*'
        elif self.swept:
            clear = '-'
        
        return clear + '['+ str(self.x) + ',' + str(self.y) + '](' + str(val) + ')'