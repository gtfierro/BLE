//
//  BluetoothBroadcast.m
//  BLE Advertise
//
//  Created by Andrew Krioukov on 9/15/14.
//  Copyright (c) 2014 Andrew Krioukov. All rights reserved.
//
//  See: https://developer.apple.com/library/ios/documentation/CoreBluetooth/Reference/CBPeripheralManager_Class/Reference/CBPeripheralManager.html#//apple_ref/occ/instm/CBPeripheralManager/startAdvertising:

#import "BluetoothBroadcast.h"

@interface BluetoothBroadcast ()
@property CBUUID *uuid;
@property CBPeripheralManager *peripheralManager;
@end

@implementation BluetoothBroadcast

- (id)initWithUUID:(NSString *)uuid
{
    self = [super init];
    if (self) {
        self.uuid = [CBUUID UUIDWithString:uuid];
        self.peripheralManager = [[CBPeripheralManager alloc] initWithDelegate:self queue:nil];
    }
    
    return self;
}

- (void)startBroadcasting
{
    NSLog(@"startBroadcasting");    
    if ([CBPeripheralManager authorizationStatus] != CBPeripheralManagerAuthorizationStatusAuthorized) {
        NSLog(@"CBPeripheralManager: Not authorized");
        return;
    }
    
    // Only two supported data types.
    // While app is in foreground, first 28 bytes of advertisingData go in initial advertisement.
    // If there is more data, the local name is put in a scan response.
    // While app is in background, advertisingData is ignored. Apple-specific data is sent in the advertisement instead.
    NSDictionary *advertisingData = @{CBAdvertisementDataLocalNameKey:@"test",
                                      CBAdvertisementDataServiceUUIDsKey:@[self.uuid]};
    [self.peripheralManager startAdvertising:advertisingData];
    
}

- (void)peripheralManagerDidUpdateState:(CBPeripheralManager *)peripheral
{
    if (peripheral.state == CBPeripheralManagerStatePoweredOn) {
        NSLog(@"peripheralManagerDidUpdateState CBPeripheralManagerStatePoweredOn");
        [self startBroadcasting];
    } else {
        NSLog(@"peripheralManagerDidUpdateState %ld", peripheral.state);
    }
}

- (void)peripheralManagerDidStartAdvertising:(CBPeripheralManager *)peripheral error:(NSError *)error
{
    NSLog(@"peripheralManagerDidStartAdvertising");
    if (error) {
        NSLog(@"Error advertising: %@", [error localizedDescription]);
    }
}
@end
