use std::sync::Arc;
//use std::sync::Mutex;
use tokio::sync::Mutex;

// This fork sets up basic data storage architecture with RocksDb/
mod kv;
mod utils;
//
// fn main() {
//    let array_set = utils::ArraySet::new_with_item(1);
//    array_set.add(2);
//    array_set.add(3);
//    array_set.add(4);
//    array_set.add(5);
//    array_set.add(6);
//
//    let res = array_set.get_all();
//
//    println!("{:?}", res);
//
//    array_set.delete(5);
//
//    let res = array_set.get_all();
//    println!("{:?}", res);
//
// }

#[tokio::main]
async fn main() {
    let value = utils::ArraySet::new_with_item(1); //kv::ArraySet::new_with_item(1);
    let array_set = Arc::new(value);// kv::ArraySet::new_with_item(1).await;
    
    array_set.add(2);
    
    //array_set.add(2).await;
    let clone_arc = Arc::clone(&array_set);
    let _r = tokio::spawn(async move {
        clone_arc.add(7);
    }).await;

    let clone2 = array_set.clone();
    let _r2 = tokio::spawn(async move {
        clone2.add(12);
    }).await;
    

    let res = array_set.get_all();
    // let res = vec.get_all();

    println!("{:?}", res);
}

