def isCollision(object_above, object_below, Floor_value):
    if object_above.food_name == "Under-bun":
        if object_above.yPosition > Floor_value:
            return True
    elif object_below.yPosition - object_below.height / 2 < object_above.yPosition + object_above.height:
        return True
    else: return False

def check_collisions(main_object, object_below, rebote, Floor_value):

    if isCollision(main_object, object_below, Floor_value):
        main_object.calculo_rebote = -(abs(main_object.spdy) * rebote)
        
        if main_object.calculo_rebote < -1.5:
            main_object.spdy = main_object.calculo_rebote
            main_object.yPosition += main_object.spdy
        else:
            main_object.spdy = 0

            if object_below.move == False:
                main_object.move = False

        while isCollision(main_object, object_below, Floor_value):
            main_object.yPosition -= 1