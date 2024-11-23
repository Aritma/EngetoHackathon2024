import { DiffFilled, HeartFilled } from "@ant-design/icons";
import { Button, ConfigProvider, Typography } from "antd";
import Flex from "antd/es/flex";
import React from "react";

const { Text } = Typography;
interface ITask {
  id: string;
  title: string;
  subtitle: string;
  description:string;
  status: string;
  reward: number;
  isDone: boolean;
  callback: (id: string) => void;
}
export const Task: React.FC<ITask> = ({
  id,
  title,
  subtitle,
  reward,
  description,
  isDone,
  status,
  callback,
}) => {
  return (
    <div
      style={{
        width: "100%",
        padding: 12,
        border: "1px solid #eaeaea",
        borderRadius: 10,
        background: isDone && "#589e3e21",
      }}
    >
      <Flex gap={20} justify="space-between" align="center">
        <Flex gap={20} align="center">
          <Flex
            align="center"
            justify="center"
            style={{
              width: 50,
              height: 50,
              background: "#ffbf0a",
              borderRadius: 15,
            }}
          >
            {isDone ? (
              <HeartFilled
                style={{ color: "red", fontWeight: "bolder", fontSize: 25 }}
              />
            ) : (
              <DiffFilled
                style={{ color: "green", fontWeight: "bolder", fontSize: 25 }}
              />
            )}
          </Flex>
          <Flex vertical style={{ width: 450 }}>
            <Text
              style={{ fontSize: 22, fontWeight: "bolder", color: "black" }}
            >
              {title}
            </Text>
            <Text style={{ fontSize: 16, fontWeight: "normal", color: "gray" }}>
              {description}
            </Text>
          </Flex>

          {!isDone && (
            <Flex vertical style={{ marginLeft: 40 }}>
              <Text
                style={{ fontSize: 22, fontWeight: "bolder", color: "black" }}
              >
                Odměna
              </Text>
              <Text
                style={{
                  fontSize: 16,
                  fontWeight: "900",
                  textAlign: "center",
                  borderRadius: 16,
                  color: "white",
                  background: isDone ? "#589e3e" : "#ffbe07",
                }}
              >
                {reward} Kč
              </Text>
            </Flex>
          )}
        </Flex>

        <ConfigProvider
          theme={{
            token: {
              colorPrimary: "#ffbf0a",
            },
          }}
        >
          {!isDone ? (
            <Button
              size="large"
              style={{ fontWeight: "bold" }}
              variant="filled"
              onClick={() => callback(id)}
            >
              Mám hotovo 🎉
            </Button>
          ) : (
            <Flex align="center" gap={12}>
              <Text
                style={{ fontSize: 22, fontWeight: "bolder", color: "black" }}
              >
                Získané penízky:
              </Text>
              <Text
                style={{
                  fontSize: 16,
                  fontWeight: "900",
                  textAlign: "center",
                  borderRadius: 16,
                  padding: 10,
                  color: "white",
                  background: isDone ? "#589e3e" : "#ffbe07",
                }}
              >
                {reward}{status === "waiting" ? '+' : ''}{status === "waiting" ? (reward/100)*20 : ''} Kč
              </Text>
              {status === "waiting" && (
                <Text
                  style={{
                    fontSize: 16,
                    fontWeight: "900",
                    textAlign: "center",
                    borderRadius: 16,
                    padding: 10,
                    color: "white",
                    background: isDone ? "#589e3e" : "#ffbe07",
                  }}
                >
                Spořím
                </Text>
              )}
            </Flex>
          )}
        </ConfigProvider>
      </Flex>
    </div>
  );
};
