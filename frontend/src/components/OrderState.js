// Using the State design pattern for an Order object
// This file manages their states

import axios from "axios";

export class OrderState {
    constructor(order) {
        this.states = [
            new NewOrder(), 
            new PreparingOrder(), 
            new ReadyOrder(),
            new DispatchedOrder(), 
            new DeliveredOrder(),
            new CancelledOrder()
        ];

        // set default state
        if (order === undefined) {
            this.current = this.states[0];
        }
        else {
            switch (order.orderStatus) {
                case 'new':
                    this.current = this.states[0];
                    break;
                case 'preparing':
                    this.current = this.states[1];
                    break;
                case 'ready':
                    this.current = this.states[2];
                    break;
                case 'dispatched':
                    this.current = this.states[3];
                    break;
                case 'delivered':
                    this.current = this.states[4];
                    break;
                case 'cancelled':
                    this.current = this.states[5];
                    break;
            }
        }
    }

    // change state
    change(order, state) {
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

        axios
        .put(`${process.env.API_URL}api/order`, {
            id: order.id,
            orderStatus: this.current.order
        })
        .then(
            response => { 
                console.log(response)
            },
            error => {
                console.log(error);
                errorMsg = "Order cannot be updated.";
            }
        );
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

    chefAcceptsOrder(order, state) {
        state.change(order, new PreparingOrder());
        location.reload(true);
    }
}

class PreparingOrder extends Order {
    constructor() {
        super('preparing');
    }

    chefUpdateOrder(order, state) {
        state.change(order, new ReadyOrder());
        location.reload(true);
    }

    cancelOrder(order, state) {
        if (currentTime() > timeOrdered)
            state.change(order, new CancelledOrder());
        else
            return "Order cannot be cancelled!";
    }
}

class ReadyOrder extends Order {
    constructor() {
        super('ready');
    }

    dispatcherAcceptsOrder(order, state) {
        state.change(order, new DispatchedOrder());
    }

    cancelOrder(order, state) {
        if (currentTime() > timeOrdered)
            state.change(order, new CancelledOrder());
        else
            return "Order cannot be cancelled!";
    }
}

class DispatchedOrder extends Order {
    constructor() {
        super('dispatched');
    }

    updateDeliveryStatus(order, state) {
        state.change(order, new DeliveredOrder());
    }

    cancelOrder(order, state) {
        if (currentTime() > timeOrdered)
            state.change(order, new CancelledOrder());
        else
            return "Order cannot be cancelled!";
    }
}

class DeliveredOrder extends Order {
    constructor() {
        super('delivered');
    }
}

class CancelledOrder extends Order {
    constructor() {
        super('cancelled');
    }
}

export function currentTime() {
    var today = new Date();
    var currentTime = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    return currentTime;
}