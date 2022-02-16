import { useState, useEffect } from "react";
import Boundingbox from "react-bounding-box";
import client from "../Client";
import { Layout, Spin, Row, Col, Card, Switch, Button } from "antd";
import "antd/dist/antd.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { CirclePicker } from "react-color";
import boxOptions from "../utils/options";
import { Header } from "antd/lib/layout/layout";

const ImageDisplayNew = () => {
  const [image, setImage] = useState(null);
  const [options, setOptions] = useState(boxOptions);
  const [selected, setSelected] = useState(false);
  const [imageObject, setImageObject] = useState();
  const [boxes, setBoxes] = useState([]);
  const [display, setDisplay] = useState([]);
  const [loading, setLoading] = useState(false);
  const [detected, setDetected] = useState(true);

  useEffect(() => {
    if (image) {
      setImage(image);
    }
  }, [image]);

  const handleSelect = (e) => {
    e.preventDefault();
    setImage(null);
    if (e.target.files.length > 0) {
      setImageObject(e.target.files[0]);
      setSelected(true);
      setImage(URL.createObjectURL(e.target.files[0]));
      return;
    }
    setImage(image);
  };

  const handleSwitch = (value) => {
    if (value) {
      setDisplay([...boxes]);
      return;
    }
    setDisplay([]);
  };

  const handlePick = (object) => {
    const rgb = object.rgb;
    const colorString = `rgba(${rgb.r},${rgb.g},${rgb.b},${rgb.a})`;
    const colors = {
      normal: colorString,
      selected: colorString,
      unselected: colorString,
    };
    setOptions({ ...options, colors });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    setLoading(true);
    const data = new FormData();
    data.append("file", imageObject);
    client
      .post("http://localhost:8001/detect/", data)
      .then((response) => {
        if (response.status === 200) {
          const predictions = response.data;
          const detections = predictions.map((item) => {
            const box = item[2];
            const x = box[0] - box[2] / 2;
            const y = box[1] - box[3] / 2;
            const w = box[2];
            const h = box[3];
            return [x, y, w, h];
          });
          setImage(image);
          setBoxes(detections);
          setDisplay(detections);
          setDetected(false);
          setLoading(false);
        }
      })
      .catch((error) => {
        console.log("error ", error);
      });
  };

  return (
    <>
      <Layout>
        <Header style={{ color: "white", width: "100%" }}>
          Vertebrae Counter
        </Header>
      </Layout>
      <Layout>
        <Row
          style={{
            height: "93vh",
          }}
          justify="center"
          gutter={[16, 16]}
        >
          <Col
            span={20}
            flex="1 0 25%"
            style={{
              height: "100%",
              overflow: "scroll",
            }}
          >
            <div>
              <Button onClick={handleSubmit} type="primary" block>
                Send
              </Button>
              <input type="file" onChange={handleSelect} />
              <Spin spinning={loading} tip="Counting vertebrae...">
                {selected && (
                  <div
                    style={{
                      display: "flex",
                      width: "100%",
                      height: "100%",
                      overflow: "hidden",
                      justifyContent: "center",
                      alignItems: "center",
                    }}
                  >
                    <Boundingbox
                      image={image}
                      boxes={display}
                      options={options}
                    />
                  </div>
                )}
              </Spin>
            </div>
          </Col>
          <Col
            span={4}
            flex="1 0 25%"
            style={{
              height: "100%",
            }}
          >
            <Card>
              <h2>Vertebrae Count</h2>
              <p style={{ fontSize: "5rem", textAlign: "center" }}>
                {boxes.length ? boxes.length : 0}
              </p>
            </Card>
            <Card
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <h2 style={{ textAlign: "center" }}>Toggle Detections</h2>
              <div style={{ marginLeft: "40%" }}>
                <Switch
                  disabled={detected}
                  checkedChildren="On"
                  unCheckedChildren="Off"
                  onChange={handleSwitch}
                  defaultChecked
                />
              </div>
            </Card>
            <Card>
              <h2 style={{ textAlign: "center" }}>Color Picker</h2>
              <div>
                <CirclePicker onChange={handlePick} />
              </div>
            </Card>
          </Col>
        </Row>
      </Layout>
    </>
  );
};
export default ImageDisplayNew;
