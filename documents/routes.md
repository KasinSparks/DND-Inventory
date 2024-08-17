# Routes

## home


## admin
* users
* users/<string:username>
* users/remove
* users/makeAdmin
* users/verify/<int:user_id>

* notifications
* notifications/remove/<int:notification_id>
* notifications/markRead/<int:notification_id>

* items/approveAllItems
* items/approveItem/<int:item_id>/<int:status>


## auth
* reset/sq
* reset/newpass

* set/newquestions

* register

* login
* logout

* register/tos
* register/tos/accept


## character
* select

* <int:char_id>

* create
* create/submit

* edit/class/<int:char_id>
* edit/race/<int:char_id>
* edit/alignment/<int:char_id>
* edit/level/<int:char_id>
* edit/currency/<int:char_id>
* edit/image/<int:char_id>
* edit/health/<int:char_id>
* edit/resource/<int:char_id>
* edit/maxhealth/<int:char_id>
* edit/ac/<int:char_id>
* edit/initiative/<int:char_id>
* edit/attackBonus/<int:char_id>
* edit/str/<int:char_id>
* edit/dex/<int:char_id>
* edit/con/<int:char_id>
* edit/int/<int:char_id>
* edit/wis/<int:char_id>
* edit/cha/<int:char_id>

* add/items/<int:char_id>

* remove/items/<int:char_id>

* item/equip/<int:char_id>/<int:item_id>/<int:slot_number>
* item/unquip/<int:char_id>/<int:item_id>/<int:slot_number>/<int:remove_all>

* abilities/add
* abilities/edit
* abilities/delete

* skill/add
* skill/edit
* skill/delete

## dataserver
* equipmentItemDetails/<int:char_id>/<string:equipment_slot>

* inventoryItemDetails/<int:char_id>/<int:item_id>

* getClassName/<int:char_id>
* getRaceName/<int:char_id>
* getAlignmentOptions
* getLevel/<int:char_id>
* getHealth/<int:char_id>
* getMaxHealth/<int:char_id>
* getAC/<int:char_id>
* getResource/<int:char_id>
* getInitiative/<int:char_id>
* getAttackBonus/<int:char_id>
* getStr/<int:char_id>
* getDex/<int:char_id>
* getCon/<int:char_id>
* getInt/<int:char_id>
* getWis/<int:char_id>
* getCha/<int:char_id>
* getCurrency/<int:char_id>
* getItemList/<int:item_slot>
* getCurrentEquipedItems/<int:char_id>/<int:item_slot>
* getItemsInSlot/<int:char_id>/<string:item_slot>
* getItemAmount/<int:char_id>/<int:item_id>

* itemDetails/<int:item_id>
* itemFullDetails/<int:item_id>

## imageserver
* user/<string:image_name>

* item/<string:image_name>

## tools
* creationKit
* creationKit/add
* creationKit/add/submit
* creationKit/edit/<int:item_id>
* creationKit/edit/submit
* creationKit/remove/<int:item_id>
