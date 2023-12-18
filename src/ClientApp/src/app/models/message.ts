import { RoomDetails } from './room/room-details.mode';
import { UserDetails } from './user_details.model';
export enum MessageType {
    BROADCAST_MESSAGE = 1,
    USERNAME = 2,
    USER_MESSAGE = 3,
}

export interface Message {
    data: any;
    messageType: MessageType;
}

export interface UsernameData {
    username: string;
}

export interface BroadcastData {
    id: string;
    message: string;
    user: UserDetails;
    room: RoomDetails;
}