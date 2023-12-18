import { UserDetails } from './../user_details.model';

export interface RoomDetails {
    id: string;
    room_name: string;
    owner_id: string;
    room_status: string;
    owner: UserDetails;
}