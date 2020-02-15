// Using the State design pattern for an Order object
// This file only manages their states

export class OrderState {
    constructor() {
        this.states = [
            new NewOrder(), 
            new PreparingOrder(), 
            new ReadyOrder(),
            new DispatchedOrder(), 
            new DeliveredOrder(),
            new CancelledOrder()
        ];

        // set default state
        this.current = this.states[0];
    }

    // change state
    change(state) {
        const totalStates = this.states.length;
        let currentIndex = this.states.findIndex(order => order === this.current);
        
        // if no state is defined in the parameters, change it to the next state
        if (state != undefined) 
            this.current = state;
        else { 
            if (currentIndex + 1 < totalStates)
                this.current = this.states[currentIndex + 1];
            else
                this.current = this.states[0];
        }
    }

    sign() {
        return this.current.sign();
    }
}

export class Order {
    constructor(order) {
        this.order = order;
    }
}

class NewOrder extends Order {
    constructor() {
        super('new');
    }

    sign() {
        return 'NEW';
    }

    chefAcceptsOrder() {
        state.change(new PreparingOrder());
    }
}

class PreparingOrder extends Order {
    constructor() {
        super('preparing');
    }

    sign() {
        return 'PREPARING';
    }

    chefUpdateOrder() {
        state.change(new ReadyOrder());
    }

    cancelOrder() {
        if (currentTime() > timeOrdered)
            state.change(new CancelledOrder());
        else
            return "Order cannot be cancelled!";
    }
}

class ReadyOrder extends Order {
    constructor() {
        super('ready');
    }

    sign() {
        return 'READY';
    }

    dispatcherAcceptsOrder() {
        state.change(new DispatchedOrder());
    }

    cancelOrder() {
        if (currentTime() > timeOrdered)
            state.change(new CancelledOrder());
        else
            return "Order cannot be cancelled!";
    }
}

class DispatchedOrder extends Order {
    constructor() {
        super('dispatched');
    }

    sign() {
        return 'DISPATCHED';
    }

    updateDeliveryStatus() {
        state.change(new DeliveredOrder());
    }

    cancelOrder() {
        if (currentTime() > timeOrdered)
            state.change(new CancelledOrder());
        else
            return "Order cannot be cancelled!";
    }
}

class DeliveredOrder extends Order {
    constructor() {
        super('delivered');
    }

    sign() {
        return 'DELIVERED';
    }
}

class CancelledOrder extends Order {
    constructor() {
        super('cancelled');
    }

    sign() {
        return 'CANCELLED';
    }
}

export function currentTime() {
    var today = new Date();
    var currentTime = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    return currentTime;
}

export let state = new OrderState;