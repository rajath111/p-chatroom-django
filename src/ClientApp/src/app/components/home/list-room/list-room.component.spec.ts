import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListRoomComponent } from './list-room.component';

describe('ListRoomComponent', () => {
  let component: ListRoomComponent;
  let fixture: ComponentFixture<ListRoomComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListRoomComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListRoomComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
