use std::sync::Mutex;

pub struct ArraySet<T> {
    arr: Mutex<Vec<T>>// Mutex<Vec<T>>
}

impl<T> ArraySet<T> where T: std::cmp::PartialEq + Copy {
    pub fn add(&self, element: T) {
        let mut vec = self.arr.lock().unwrap();//.append(element);
        if vec.iter().any(|&i| i == element) {
            return;
        } else {
            vec.push(element)
        }
    }

    pub fn new_with_item(item: T) -> ArraySet<T> {
        let arry = Mutex::new(Vec::new());
        {
        let mut arr_handle = arry.lock().unwrap();
        arr_handle.push(item);
        }

        ArraySet{
            arr: arry
        }
    }

    pub fn delete(&self, element: T) {
        let mut index_to_del: Option<usize> = None;
        let mut arr = self.arr.lock().unwrap();
        for (i, e) in arr.iter().enumerate() {
            if *e == element {
                index_to_del = Some(i);
                break;
            }
        }
        if let Some(index) = index_to_del {
            arr.remove(index);
        } else {
            return;
        }
    }

   pub fn size(&self) -> usize {
       let arr = self.arr.lock().unwrap();
       arr.len()
   }

   // Write random pick

   pub fn get_all(&self) -> Vec<T> {
       let vec = self.arr.lock().unwrap();
       let vec_clone = vec.clone();
       let array: Vec<T> = vec_clone.into_iter()
                              .collect::<Vec<T>>();
        return array;
   }

   pub fn get_all_and_clear(&self) -> Vec<T> {
       let mut vec = self.arr.lock().unwrap();
       let old_vec = vec.clone();
       vec.clear();
       old_vec
   }
 
}
