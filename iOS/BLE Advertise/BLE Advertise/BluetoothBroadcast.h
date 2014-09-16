//
//  BluetoothBroadcast.h
//  BLE Advertise
//
//  Created by Andrew Krioukov on 9/15/14.
//  Copyright (c) 2014 Andrew Krioukov. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CoreBluetooth/CoreBluetooth.h>

@interface BluetoothBroadcast : NSObject <CBPeripheralManagerDelegate>
- (id)initWithUUID:(NSString *)uuid;
- (void)startBroadcasting;
- (void)peripheralManagerDidUpdateState:(CBPeripheralManager *)peripheral;
- (void)peripheralManagerDidStartAdvertising:(CBPeripheralManager *)peripheral error:(NSError *)error;
@end
