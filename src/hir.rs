use serde::{Deserialize, Serialize};
pub type StringPool = Vec<String>;
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Module {
    pub name: StringRef,
    pub functions: Vec<Function>,
}
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct StringRef(pub u32);

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Function {}
