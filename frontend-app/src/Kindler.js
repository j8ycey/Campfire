import React from "react";
import { useState } from "react";
import { useEffect } from "react";

export default function Kindler() {
	const [KindlerList, SetKindlerData] = useState([]);

	useEffect(() => {


		const KindlerData = async () => {
			const url = `${process.env.REACT_APP_USERS}/users/api/kindler`;
			const response = await fetch(url, { credentials: "include" });

			if (response.ok) {
				const data = await response.json();
				console.log("kindler data: ", data);

				// adding additional key-value pair so that we can
				// track who has been added to a clients friend list
				for (let friend of data) {
					friend.friend = false;
				}
				
				SetKindlerData(data);
			}
		};

		KindlerData();
	}, []);

	async function onClick(friendID, objectNum) {
		console.log("clicked obejctnum: ", objectNum);

		const url = `${process.env.REACT_APP_USERS}/users/api/friend/`;
		const params = {
			method: "put",
			body: friendID,
			credentials: "include",
		};
		const response = await fetch(url, params);

		if (response.status === 200) {
			let kindlerState = [...KindlerList];
			kindlerState[objectNum].friend = true;
			SetKindlerData(kindlerState);
		}
	}
	// night_fire_bonfire_campfire_spark-65309
	return (
		<>
			<div className="kindle-bg"></div>
			<div className="container px-4 py-5 my-5 text-center">
				<h1 className="kindle-text display-5 fw-bold">The Campfire Kindler</h1>
				<h3 className="kindle-text">Kindle new friendships</h3>
				<div className="col-lg-6 mx-auto">
					<div className="lead mb-4"></div>
				</div>
				{KindlerList.length > 0 ? (
					<div className="row">
						{KindlerList.slice(0).map((KindlerUser, index) => {
							return (
								<div className="col-sm-4" key={KindlerUser.id}>
									<div className="kindle-top-level-card mb-3 shadow">
										<img className="kindle-card-image" src={KindlerUser?.profile_photo || "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHPJFBrPoazCA8scTIXSLI6fwQHWFI-VhSkQ&usqp=CAU"} alt="" />
										<div className="card-body ">
											<h5 className="card-title">{KindlerUser.username}</h5>
											{!KindlerUser?.friend ? (
												<button
													type="button"
													className="btn btn-warning"
													onClick={() => {
														onClick(KindlerUser?.id, index);
													}}
												>
													{" "}
													Add to Friend's List{" "}
												</button>
											) : (
												<div>
													<h6 className="card-text">
														How to contact {KindlerUser?.username}: {KindlerUser?.email}
													</h6>
													<div style={{ padding: 5 }}>
														<h5 className="card-subtitle text-muted"> {KindlerUser?.username} added to friends list! </h5>
													</div>
												</div>
											)}
										</div>
										<div className="card-footer">
											{KindlerUser.city}-{KindlerUser.state}
										</div>
									</div>
								</div>
							);
						})}
					</div>
				) : (
					<div>
						<br />
						<br />
						<br />
						<br />
						<br />
						<br />
						<br />
						<br />
						<br />
						<br />
						<div className="kindle-top-level-card">
						<h2 className="card-text">Wow! You are already friends with everybody with similar interests!</h2>
						<h3 > You can potentially match with more friends by adding new activities. </h3>
						</div>
					</div>
				)}
			</div>
		</>
	);
}
