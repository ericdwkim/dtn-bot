 """
    <ul class="available connected-list" style="height: 172px;">
        <li class="ui-state-default ui-element ui-draggable" title="Credit Card">
        <span class="ui-helper-hidden">
        </span>Credit Card<a href="#" class="action">
        <span class="ui-corner-all ui-icon ui-icon-plus">
        </span>
        </a>
        </li>
    <li class="ui-state-default ui-element ui-draggable" title="Draft Notice">
    <span class="ui-helper-hidden"></span>Draft Notice<a href="#" class="action">
    <span class="ui-corner-all ui-icon ui-icon-plus"></span></a></li><li class="ui-state-default ui-element ui-draggable" title="Invoice">
    <span class="ui-helper-hidden"></span>Invoice<a href="#" class="action"><span class="ui-corner-all ui-icon ui-icon-plus"></span></a></li>
    <li class="ui-state-default ui-element ui-draggable" title="Price"><span class="ui-helper-hidden"></span>Price<a href="#" class="action">
    <span class="ui-corner-all ui-icon ui-icon-plus"></span></a></li><li class="ui-state-default ui-element ui-draggable" title="Rack Report">
    <span class="ui-helper-hidden"></span>Rack Report<a href="#" class="action"><span class="ui-corner-all ui-icon ui-icon-plus"></span></a></li></ul>
    
    @dev: above is the full copied element of the unordered list for *all* existing draggable bars for the `Group` filter
    1) get XPATH syntax down for this ul element so that it returns a <List>WebElements
                # desired element at idx 1
                //ul[@class='available connected-list']
    2) access desired idx from list (Credit Card, Draft Notice, Invoice, Price, Rack Report)
    3) this will allow this new helper fn to be reusable for all `Group` filter setting use cases and NOT just for Invoice
    """