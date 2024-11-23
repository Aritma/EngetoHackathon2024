import { Card, ConfigProvider, Flex, Modal, Typography } from "antd";
import apiCall from "../../api/apiCall";
import Title from "antd/es/typography/Title";
import { Task } from "../Task";
import girafe from "../../assets/giraf.png";
import { useEffect, useState } from "react";

const { Text } = Typography;
interface IUser {
  user_id: string;
  name: string;
  balance: string;
  role: string;
}
const UdrzitelnyPrehled = () => {
  const [data, setData] = useState<
    Array<{
      created_at: string;
      done_by: string;
      is_done: boolean;
      description:string;
      status: string;
      reward_amount: number;
      task_id: number;
      task_name: string;
    }>
  >(null);

  const [userData, setUserdata] = useState<IUser>(null);

  const [isModalOpen, setModalOpen] = useState<boolean>(false);
  const [selectedTask, setSelectedTask] = useState<{
    created_at: string;
    done_by: string;
    is_done: boolean;
    status: string;
    reward_amount: number;
    task_id: number;
    task_name: string;
  }>(null);
  const handleOnClick = () => {
    const getData = async () => {
      try {
        const URI = `http://127.0.0.1:5000/all_tasks?user_id=2`; //Change the URL
        const response = await apiCall(URI, { method: "GET" }); // By default method is get
        console.log(response);
        setData(response);
      } catch (error) {}
    };
    getData();
  };

  const getUser = () => {
    const getData = async () => {
      try {
        const URI = `http://127.0.0.1:5000/my_data?user_id=2`; //Change the URL
        const response = await apiCall(URI, { method: "GET" }); // By default method is get
        console.log(response);
        setUserdata(response);
      } catch (error) {
        console.log("fasfa");
      }
    };
    getData();
  };
  const handleReload = () => {
    handleOnClick();
    getUser();
  };
  useEffect(() => {
    handleReload();
  }, []);

  const getTaskDoneCount = () => {
    if (!data) return;

    return data.length - data.filter((item) => item.is_done === false).length;
  };

  const handleDoneTask = (id: string) => {
    const sData = data.find((item) => item.task_id === Number(id));
    setSelectedTask(sData);
    setModalOpen(true);
  };

  const getWaitingMoney = () => {
    if (!data) return;
    const myData = data.filter((item) => item.status === "waiting");
    const moneySum = myData.reduce((acc, item) => {
      return acc + item.reward_amount;
    }, 0);
    return moneySum;
  };

  const handleSetTaskDone = async (id: string, wait: boolean) => {
    const URI = `http://127.0.0.1:5000/do_task/${id}?user_id=2&pay_now=${
      wait ? "true" : "false"
    }`; //Change the URL
    const response = await apiCall(URI, { method: "POST" }); // By default method is get
    setModalOpen(false);
    handleReload();
  };

  return (
    <ConfigProvider
      theme={{
        token: {
          fontFamily: "Nunito",
        },
      }}
    >
      <div>
        <Title style={{ fontWeight: "bold" }}>Adámkova nástěnka</Title>
        <Flex gap={30}>
          <Card style={{ backgroundColor: "#ffbf0a", width: "100%" }}>
            <Flex vertical>
              <Text
                style={{
                  fontSize: 34,
                  fontWeight: "bolder",
                  color: "white",
                  textShadow: "0px 2px 9px #c59409",
                }}
              >
                Celkem peněz
              </Text>

              <div style={{marginTop:12}}>
              <Text
                  style={{
                    fontSize: 34,
                    fontWeight: "bolder",
                    color: "#1d860c",
                    padding: 10,
                    background: "#ebf2e7",
                    borderRadius: 16,
                  }}
                >
                  {userData?.balance} Kč
                </Text>
              </div>
            </Flex>
            <img
              width={100}
              src={girafe}
              style={{ position: "absolute", bottom: 0, right: 0, width: 60 }}
              alt="fireSpot"
            />
          </Card>

          <Card style={{ backgroundColor: "#ffbf0a", width: "100%" }}>
            <Flex vertical>
              <Text
                style={{
                  fontSize: 34,
                  fontWeight: "bolder",
                  color: "white",
                  textShadow: "0px 2px 9px #c59409",
                }}
              >
                Spoření a bonus
              </Text>

              <div style={{marginTop:12}}>
                <Text
                  style={{
                    fontSize: 34,
                    fontWeight: "bolder",
                    color: "#1d860c",
                    padding: 10,
                    background: "#ebf2e7",
                    borderRadius: 16,
                  }}
                >
                  {getWaitingMoney()} Kč
                </Text>
                <Text
                  style={{
                    fontSize: 34,
                    fontWeight: "bolder",
                    color: "#1d860c",
                    padding: 12,
                    borderRadius: 16,
                  }}
                >
                  +
                  </Text>
                <Text
                  style={{
                    fontSize: 34,
                    fontWeight: "bolder",
                    color: "#1d860c",
                    padding: 10,
                    background: "#ebf2e7",
                    borderRadius: 16,
                  }}
                >
                  {(getWaitingMoney()/ 100) * 20} Kč
                </Text>
              </div>
            </Flex>
            
          </Card>
          {/* <Card style={{ backgroundColor: "#ffbf0a", width: "100%" }}>
            <Flex vertical>
              <Text
                style={{
                  fontSize: 34,
                  fontWeight: "bolder",
                  color: "white",
                  textShadow: "0px 2px 9px #c59409",
                }}
              >
                Peníze ze spoření
              </Text>

              <div style={{marginTop:12}}>
              <Text
                  style={{
                    fontSize: 34,
                    fontWeight: "bolder",
                    color: "#1d860c",
                    padding: 12,
                    background: "#ebf2e7",
                    borderRadius: 16,
                  }}
                >
                  {(getWaitingMoney()/ 100) * 20} Kč
                </Text>
              </div>
            </Flex>
            <img
              width={100}
              src={girafe}
              style={{ position: "absolute", bottom: 0, right: 0, width: 60 }}
              alt="fireSpot"
            />
          </Card> */}

          <Card style={{ backgroundColor: "#ffbf0a", width: "100%" }}>
            <Flex vertical>
              <Text
                style={{
                  fontSize: 34,
                  fontWeight: "bolder",
                  color: "white",
                  textShadow: "0px 2px 9px #c59409",
                }}
              >
                Splněných úkolů
              </Text>
              <div style={{marginTop:12}}>
              <Text
                  style={{
                    fontSize: 34,
                    fontWeight: "bolder",
                    color: "#1d860c",
                    padding: 12,
                    background: "#ebf2e7",
                    borderRadius: 16,
                  }}
                >
                  {getTaskDoneCount()} z {data && data.length}
                </Text>
              </div>
            </Flex>
          </Card>
        </Flex>

        <div style={{ margin: 16 }}>
          <Text style={{ fontSize: 34, fontWeight: "bolder", color: "black" }}>
            Úkoly
          </Text>
        </div>
        <Flex gap={30} vertical>
          {data &&
            data
              .filter((item) => item.is_done === false)
              .map((item) => {
                return (
                  <Task
                    id={item.task_id.toString()}
                    callback={handleDoneTask}
                    title={item.task_name}
                    status={item.status}
                    description={item.description}
                    subtitle="Správně udělat úkol"
                    reward={item.reward_amount}
                    isDone={!!item.done_by}
                  ></Task>
                );
              })}
        </Flex>

        <div style={{ margin: 16 }}>
          <Text style={{ fontSize: 34, fontWeight: "bolder", color: "black" }}>
            Splněné úkoly
          </Text>
        </div>
        <Flex gap={30} vertical>
          {data &&
            data
              .filter((item) => item.is_done === true)
              .map((item) => {
                return (
                  <Task
                    id={item.task_id.toString()}
                    callback={handleDoneTask}
                    status={item.status}
                    description={item.description}
                    title={item.task_name}
                    subtitle="Správně udělat úkol"
                    reward={item.reward_amount}
                    isDone={!!item.done_by}
                  ></Task>
                );
              })}
        </Flex>
      </div>
      <Modal
        width={660}
        open={isModalOpen}
        title="Super práce, jsi Hrdina!"
        onOk={() => {}}
        onCancel={() => {
          setModalOpen(false);
        }}
        footer={[]}
      >
        <Flex style={{ marginTop: 20, marginBottom: 80 }} gap={20}>
          <Flex vertical>
            <Text style={{ fontSize: 16, fontWeight: "normal" }}>
              Mamka a taťka ti děkují za splnění úkolu -{" "}
              <b>{selectedTask?.task_name}</b>! Teď si to zkontrolují a potvrdí
              odměnu.
            </Text>
            <Text style={{ fontSize: 22, marginTop: 20, fontWeight: "bold" }}>
              Chceš si vzít odměnu rovnou nebo
              <span
                style={{
                  background: "#ffbf0a",
                  paddingLeft: 5,
                  paddingRight: 5,
                }}
              >
                výplatu odložíš o 5 dní, budeš spořit
              </span>
              a budeš mít o 20% víc peněz?
            </Text>
            <Flex
              gap={20}
              align="center"
              justify="center"
              style={{ marginTop: 40 }}
            >
              <Flex
                onClick={() =>
                  handleSetTaskDone(selectedTask.task_id.toString(), true)
                }
                vertical
                align="center"
                style={{
                  borderRadius: 20,
                  border: "3px solid #ffbf0a",
                  cursor: "pointer",
                  width: 120,
                  height: 80,
                  padding: 16,
                }}
              >
                <Text style={{ fontSize: 18, fontWeight: "bold" }}>
                  Beru hned
                </Text>
                <Text style={{ fontSize: 35, fontWeight: "bold" }}>
                  {selectedTask?.reward_amount} Kč
                </Text>
              </Flex>
              <Flex
                onClick={() =>
                  handleSetTaskDone(selectedTask.task_id.toString(), false)
                }
                vertical
                align="center"
                style={{
                  cursor: "pointer",
                  borderRadius: 20,
                  background: "#ffbf0a",
                  width: 120,
                  height: 80,
                  padding: 16,
                }}
              >
                <Text style={{ fontSize: 18, fontWeight: "bold" }}>Spořím</Text>

                <Text
                  style={{
                    fontSize: 35,
                    textAlign: "center",
                    fontWeight: "bold",
                  }}
                >
                  {selectedTask?.reward_amount +
                    (selectedTask?.reward_amount / 100) * 20}{" "}
                  Kč
                </Text>
              </Flex>
            </Flex>
          </Flex>
          <img width={180} src={girafe} alt="fireSpot" />
        </Flex>
      </Modal>
    </ConfigProvider>
  );
};

export default UdrzitelnyPrehled;
